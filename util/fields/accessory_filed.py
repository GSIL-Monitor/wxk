# encoding: utf-8

from __future__ import unicode_literals

from flask_admin.form import FileUploadField
import json
import logging
import threading
from io import BytesIO
from qiniu import put_data
from wtforms.utils import unset_value
from werkzeug._compat import text_type

from modules.proxy import proxy

from util.broker import file_remove
from util.exception import BackendServiceError, QiNiuServiceError
from ..widgets.accessory_widget import AccessoryFileuploadInput,\
        MysqlFileuploadInput, MultiFileuploadInput, MxpMultiFileuploadInput


class AccessoryFileuploadField(FileUploadField):

    widget = AccessoryFileuploadInput()


class MysqlFileUploadField(FileUploadField):

    widget = MysqlFileuploadInput()

    def __init__(self, *args, **kwargs):
        namegen = secure_filename_cn
        super(MysqlFileUploadField, self).__init__(namegen=namegen, **kwargs)

    def get_info(self, filename):
        return {"docType": self.file_type,
                "fileName": filename}

    def _save_file(self, data, file_name):
        if file_name:
            info = self.get_info(file_name)
            url = "/v1/file-access/upload"
            resp = proxy.create(info, url)
            try:
                self.token = resp.json().get("token")
                self.key = resp.json().get("key")
                self.save_key = resp.json().get("saveKey")
                ret, info = put_data(self.token, self.key, data)
            except:
                raise Exception("Please contact the service maintainer.")
            return file_name

    def populate_obj(self, obj, name):
        super(MysqlFileUploadField, self).populate_obj(obj, name)
        if self.data and not isinstance(self.data, unicode):
            filename = self.data.filename
            filestr = 'name:{},key:{}'.format(filename, self.save_key)
            setattr(obj, name, filestr)

    def _delete_file(self, filename):
        pass


class TechMaterialUploadField(MysqlFileUploadField):

    def process(self, formdata, data=unset_value):

        try:
            self.file_type = formdata.getlist('fileResourceType')[0]
        except:
            self.file_type = ''
        super(TechMaterialUploadField, self).process(formdata, data)


class TrainigMaterialFileuploadField(MysqlFileUploadField):

    def process(self, formdata, data=unset_value):
        try:
            self.file_type = formdata.getlist('trainFileResourceType')[0]
        except:
            self.file_type = ''
        super(TrainigMaterialFileuploadField, self).process(formdata, data)

    def get_info(self, filename):
        return {"docType": self.file_type,
                "fileName": filename,
                "unrelateDoc": True}


class TrainigPlanFileuploadField(MysqlFileUploadField):

    def get_info(self, filename):
        return {"docType": '培训资料',
                "fileName": filename,
                "unrelateDoc": True}


class MultiFileuploadField(FileUploadField):

    # 使用该Field的一定要在视图函数中一定要加入额外js
    # extra_js
    # '/static/js/upload_file.js'

    widget = MultiFileuploadInput()

    def __init__(self, *args, **kwargs):

        namegen = secure_filename_cn
        super(MultiFileuploadField, self).__init__(namegen=namegen, **kwargs)

    def process(self, formdata, data=unset_value):

        self.store = []
        self.old_file = []

        self.process_errors = []
        if data is unset_value:
            try:
                data = self.default()
            except TypeError:
                data = self.default

        self.object_data = data

        try:
            self.process_data(data)
        except ValueError as e:
            self.process_errors.append(e.args[0])

        if formdata:
            try:
                upload = []
                self.get_fileTpye(formdata)
                for key in formdata:
                    if key.startswith('acce'):
                        if formdata.getlist(key)[0]:
                            upload.append(formdata.getlist(key)[0])
                self.raw_data = upload
                self.process_formdata(self.raw_data)
            except ValueError as e:
                self.process_errors.append(e.args[0])

        try:
            for filter in self.filters:
                self.data = filter(self.data)
        except ValueError as e:
            self.process_errors.append(e.args[0])

    def process_formdata(self, valuelist):
        data_list = []

        for data in valuelist:
            if self._is_uploaded_file(data):
                data_list.append(data)
            else:
                if isinstance(data, (str, unicode)):
                    self.old_file.append(json.loads(data))

        self.data = data_list

    def _delete_file(self, filename):
        if self.object_data:
            object_data = set([json.dumps(f) for f in json.loads(self.object_data)])
            old_file = set([json.dumps(f) for f in self.old_file])
            for del_file in list(object_data - old_file):
                if del_file:
                    item = json.loads(del_file)
                    try:
                        file_remove(key=item.get('key'), name=item.get('name'))
                    except Exception as ex:
                        logging.warn(ex)
                        raise BackendServiceError("Please contact the service maintainer.")

    def populate_obj(self, obj, name):

        self._delete_file('name')
        if self.data and not isinstance(self.data, unicode):
            for file_data in self.data:
                filename = self.generate_name(obj, file_data)
                filename = self._save_file(file_data, filename)

        self.store = self.result(self.store)
        setattr(obj, name, self.store)

    def get_info(self, filename):
        return {"docType": self.file_type,
                "fileName": filename}

    def _save_file(self, data, file_name):
        if file_name:
            info = self.get_info(file_name)
            url = "/v1/file-access/upload"
            resp = proxy.create(info, url)
            if resp.status_code != 200:
                raise BackendServiceError("file-access api has someting wrong")
            token = resp.json().get("token")
            key = resp.json().get("key")
            save_key = resp.json().get("saveKey")
            ret, info = put_data(token, key, bytes(data.stream.read()))
            if info.status_code != 200:
                logging.warn(token)
                logging.warn(save_key)
                logging.warn(ret)
                logging.warn(info)
                raise QiNiuServiceError("qiniu service have something wrong")
            self.store.append({'name': file_name, 'key': save_key})
            return file_name

    def result(self, re_list):

        re_list.extend(self.old_file)
        return json.dumps(re_list)

    def get_fileTpye(self, formdata):
        pass


class MxpMultiFileuploadField(MultiFileuploadField):

    widget = MxpMultiFileuploadInput()

    def process(self, formdata, data=unset_value):

        self.process_errors = []
        self.saveData = []
        self.formData = formdata

        if data is unset_value:
            try:
                data = self.default()
            except TypeError:
                data = self.default

        self.object_data = data

        try:
            self.process_data(data)
        except ValueError as e:
            self.process_errors.append(e.args[0])

        if formdata:
            try:
                upload = []
                self.get_fileTpye(formdata)
                for key in formdata:
                    if key.startswith('acce'):
                        upload.append(formdata.getlist(key)[0])
                self.raw_data = upload
                self.process_formdata(self.raw_data)
            except ValueError as e:
                self.process_errors.append(e.args[0])

        self.populate_obj(formdata, self.name)

        try:
            for filter in self.filters:
                self.data = filter(self.data)
        except ValueError as e:
            self.process_errors.append(e.args[0])

    def result(self, re_list):
        return re_list

    def process_formdata(self, valuelist):

        data_list = []
        old_file_list = []
        res_list = []

        for data in valuelist:
            if self._is_uploaded_file(data):
                data_list.append(data)
            else:
                if isinstance(data, (str, unicode)) and data:
                    old_file_list.append(json.loads(data))

        for data in data_list:
            data_dict = self.generate_data(data)
            self.saveData.append(data_dict)
            res_list.append({'name': data_dict.get('data').filename,
                             'key': data_dict.get('save_key')})

        self.old_file = old_file_list
        res_list.extend(old_file_list)
        self.data = res_list

    def generate_data(self, data):
        info = {"docType": "维修方案",
                "fileName": data.filename}
        url = "/v1/file-access/upload"
        resp = proxy.create(info, url)
        if resp.status_code != 200:
            raise BackendServiceError("file-access api has someting wrong")
        token = resp.json().get("token")
        key = resp.json().get("key")
        save_key = resp.json().get("saveKey")
        return {'data': data, 'token': token, 'key': key, 'save_key': save_key}

    def _save_file(self, data, file_name=None):
        if file_name:
            token = data.get("token")
            key = data.get("key")
            save_key = data.get("saveKey")
            ret, info = put_data(token, key, bytes(data.get('data').stream.read()))
            if info.status_code != 200:
                raise QiNiuServiceError("qiniu service have something wrong")

    def _delete_file(self, filename):
        if self.formData and self.object_data:
            object_data = set([json.dumps(f) for f in self.object_data])
            old_file = set([json.dumps(f) for f in self.old_file])
            del_files = list(object_data - old_file)
            for del_file in del_files:
                item = json.loads(del_file)
                file_name = item.get('name')
                key = item.get('key')
                try:
                    file_remove(key=key, name=file_name)
                except:
                    raise BackendServiceError("Please contact the service maintainer.")

    def populate_obj(self, obj, name):

        self._delete_file(name)
        for file_data in self.saveData:
            filename = self.generate_name(obj, file_data.get('data'))
            filename = self._save_file(file_data, filename)


class TechMaterialMultiFileuploadField(MultiFileuploadField):

    def get_fileTpye(self, formdata):
        self.file_type = '临时技术资料'


class TrainigPlanMultiFileuploadField(MultiFileuploadField):

    def get_info(self, filename):
            return {"docType": '培训资料',
                    "fileName": filename,
                    "unrelateDoc": True}


class TrainigMaterialMultiFileuploadField(MultiFileuploadField):

    def get_fileTpye(self, formdata):
        self.file_type = formdata.getlist('trainFileResourceType')[0]

    def get_info(self, filename):
        return {"docType": self.file_type,
                "fileName": filename,
                "unrelateDoc": True}


def secure_filename_cn(obj, file_data):

    filename = file_data.filename
    if isinstance(filename, text_type):
        from unicodedata import normalize
        filename = normalize('NFKD', filename).encode('utf-8', 'ignore')
        filename = filename.decode('utf-8')
    return filename


class AirworthinessFileuploadField(MultiFileuploadField):
    def get_info(self, filename):
        return {"docType": '适航文件',
                "fileName": filename,
                "unrelateDoc": True}


class EngineeringOrderFileuploadField(MultiFileuploadField):

    def get_info(self, filename):
        return {"docType": '工程指令',
                "fileName": filename,
                "unrelateDoc": True}


class CompanyDayRecordFileuploadField(MultiFileuploadField):

    def get_info(self, filename):
        return {"docType": '飞行日志',
                "fileName": filename,
                "unrelateDoc": True}


class AirmaterialFileuploadField(MultiFileuploadField):
    def get_info(self, filename):
        return {"docType": '航材',
                "fileName": filename,
                "unrelateDoc": True}


class StorageOrOutPutMulitFileuploadField(AirmaterialFileuploadField):
    def _delete_file(self, filename):
        pass


class RoutineWorkFileuploadField(MultiFileuploadField):
    def get_info(self, filename):
        return {"docType": "例行工作",
                "fileName": filename,
                "unrelateDoc": True}
