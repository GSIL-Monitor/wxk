# coding: utf-8

from __future__ import unicode_literals
from copy import deepcopy

from modules.models.base import Model
from modules.flows.operations import *
from modules.models.airmaterial import (
    Storage, AirmaterialList, LendApplication, PurchaseApplication,
    ReturnMaterialOrder, DisassembleOrder, AirmaterialCategory,
    BorrowingInReturnModel, PutOutStoreModel, AssembleApplication,
    LoanReturnOrder, LoanApplicationOrder, Assemble, RepairApplication,
    RepairReturnOrder, Manufacturer, Scrap, AirMaterialStorageList,
    Supplier, RepairSupplier,
)
from modules.models.project_tech.airworthiness import Airworthiness
from modules.models.project_tech.tech_material import TechMaterial
from modules.models.project_tech.training_archive import TrainingArchive
from modules.models.project_tech.training_material import TrainigMaterial
from modules.models.project_tech.training_plan import TrainingPlan
from modules.models.project_tech.retain import Retain
from modules.models.production.routine_work import RoutineWork
from modules.models.production.company_day_record import CompanyDayRecord
from modules.models.production.maintenance_record import MaintenanceRecord
from modules.models.production.fault_reports import FaultReports
from modules.models.production.troubleshooting import TroubleShooting
from modules.models.production.examine_repair_record import ExamineRepairRecord
from modules.models.basic_data.airport import Airport
from modules.models.basic_data.fly_nature import FlyNature
from modules.models.basic_data.formula import Formula
from modules.models.basic_data.pilot import Pilot
# from modules.models.basic_data.mission_nature import MissionNature
from modules.models.basic_data.pesticide import Pesticide
# from modules.models.basic_data.plane_type import PlaneType
from modules.models.project_tech.engineering_order import EngineeringOrder
from modules.models.quality.reserved_fault import ReservedFault
from modules.models.notification.announcement import Announcement
from modules.models.notification.notice import Notice

only_view_perms = [View]

basic_perms = [Create, Edit, View, Delete]

finish_perms = deepcopy(basic_perms)
finish_perms.extend([Finish])

send_perms = deepcopy(basic_perms)
send_perms.extend([Send])

bound_perms = deepcopy(basic_perms)
bound_perms.extend([EditBoundStatus, RemoveBoundStatus])

one_approve_perms = deepcopy(basic_perms)
one_approve_perms.extend([Submit, Cancel, Review, Approve])

approve_can_edit_perms = deepcopy(one_approve_perms)
approve_can_edit_perms.remove(Approve)

two_approve_perms = deepcopy(one_approve_perms)
two_approve_perms.extend([SecondApproved])

ad_approve_perms = deepcopy(one_approve_perms)
ad_approve_perms.extend([CreateEO, Sent, Receive])

eo_approve_perms = deepcopy(one_approve_perms)
eo_approve_perms.extend([Sent, Receive, CreateMR])

st_approve_perms = deepcopy(one_approve_perms)
st_approve_perms.extend([CreateST])

er_approve_perms = deepcopy(one_approve_perms)
er_approve_perms.extend([createER, Sent, Receive])

retain_approve_perms = deepcopy(one_approve_perms)
retain_approve_perms.extend([ReserveAgain, CreateRW])

reserved_approve_perms = deepcopy(one_approve_perms)
reserved_approve_perms.extend([ReserveAgain, createER])

purchase_request_perms = deepcopy(two_approve_perms)
purchase_request_perms.extend([CreateIn, UploadMeetingFile,
                               UploadContractFile])
borrow_request_perms = deepcopy(two_approve_perms)
borrow_request_perms.extend([CreateIn, UploadContractFile, ExportPDF])
borrowing_in_return_perms = deepcopy(basic_perms)
borrowing_in_return_perms.extend([Submit, Cancel, Review,
                                  CreateOut, ExportPDF])
# 借出归还
loan_return_order_perms = deepcopy(basic_perms)
loan_return_order_perms.extend([Submit, Cancel, Review,
                                CreateIn, ExportPDF])
# 借出申请
loan_application_perms = deepcopy(two_approve_perms)
loan_application_perms.extend([CreateOut, UploadContractFile,
                               CreateLR, ExportPDF])
# 装机申请
assemble_application_perms = deepcopy(finish_perms)
assemble_application_perms.extend([CreateOut, CreateAS])

# 退料单
return_material_perms = deepcopy(basic_perms)
return_material_perms.extend([PutInStore])

# 送修申请
repair_application_perms = deepcopy(one_approve_perms)
repair_application_perms.extend([CreateOut, UploadContractFile, CreateRpRt])

# 拆机单
disassemble_order_perms = deepcopy(basic_perms)
disassemble_order_perms.extend([CreateIn])

# 报废单
scrap_perms = deepcopy(two_approve_perms)
scrap_perms.extend([CreateOut])

# 检查预警
check_warning = [CheckComplete, View]
# 库存预警
stock_warning = [BorrowAppl, PurchaseAppl, View]
# 到期预警
expire_warning = [CreateScrap, View]
# 出库权限
put_out_store_perms = deepcopy(basic_perms)
put_out_store_perms.extend([OutStorePart, OutStoreFinish, ExportPDF])
# 入库权限
put_in_store_perms = deepcopy(basic_perms)
put_in_store_perms.extend([InStorePart, InStoreFinish, ExportPDF])
# 航材权限
airmaterial_record_perms = deepcopy(basic_perms)
airmaterial_record_perms.extend([AirmaterialRecord])

class AllowedOpModel(tuple):
    def __new__(_cls, model_class, display_name, actions):
        name = model_class
        if not isinstance(model_class, (str, unicode)) and\
                issubclass(model_class, Model):
            name = model_class.__name__.lower()
        return tuple.__new__(_cls, (name, display_name, actions))

    def __init__(self, model_class, *args, **kwargs):
        self.model_class = model_class


models = [
    AllowedOpModel(Airworthiness, '适航文件', ad_approve_perms),
    AllowedOpModel(TroubleShooting, '排故方案', er_approve_perms),
    AllowedOpModel(ExamineRepairRecord, '排故检修记录', finish_perms),
    AllowedOpModel(FaultReports, '故障报告', st_approve_perms),
    AllowedOpModel(TechMaterial, '技术资料', approve_can_edit_perms),
    AllowedOpModel(TrainingArchive, '培训档案', finish_perms),
    AllowedOpModel(TrainigMaterial, '培训资料', basic_perms),
    AllowedOpModel(TrainingPlan, '培训计划', one_approve_perms),
    AllowedOpModel(Retain, '保留工作', retain_approve_perms),
    AllowedOpModel(RoutineWork, '例行工作记录', finish_perms),
    AllowedOpModel(CompanyDayRecord, '单位日运行记录', finish_perms),
    AllowedOpModel(Airport, '起降机场', basic_perms),
    AllowedOpModel(FlyNature, '飞行性质', basic_perms),
    AllowedOpModel(Formula, '配方信息', basic_perms),
    AllowedOpModel(Pilot, '机长信息', basic_perms),
    AllowedOpModel(ReservedFault, '保留故障', reserved_approve_perms),
    # AllowedOpModel(MissionNature, '任务性质', basic_perms),
    AllowedOpModel(Pesticide, '农药信息', basic_perms),
    # AllowedOpModel(PlaneType, '机型信息', basic_perms),
    AllowedOpModel(Announcement, '通知公告', send_perms),
    AllowedOpModel(Notice, '短消息', send_perms),
    AllowedOpModel(MaintenanceRecord, '维护保养记录', finish_perms),
    AllowedOpModel(EngineeringOrder, '工程指令', eo_approve_perms),

    # 目前在"本地"会缓存飞行日志，然后提交到计算服务
    AllowedOpModel('flightlog', '飞行日志', finish_perms),
    AllowedOpModel('flightlogstat', '飞行时间统计', only_view_perms),
    AllowedOpModel('formulastat', '加药量统计', only_view_perms),

    # Mongo模型直接使用名称，因为不存在对应的模型定义
    AllowedOpModel('aircraft', '机队管理', bound_perms),
    AllowedOpModel('mxp', '维修方案', basic_perms),

    # 航材类权限设置
    AllowedOpModel(AirmaterialCategory, '航材类别', airmaterial_record_perms),
    AllowedOpModel(Manufacturer, '生产厂商', basic_perms),
    AllowedOpModel(Supplier, '供应商', basic_perms),
    AllowedOpModel(RepairSupplier, '维修厂商', basic_perms),
    AllowedOpModel(AirMaterialStorageList, '库存列表', only_view_perms),
    AllowedOpModel(Storage, '入库', put_in_store_perms),
    AllowedOpModel(PutOutStoreModel, '出库', put_out_store_perms),
    AllowedOpModel(PurchaseApplication, '采购申请', purchase_request_perms),
    AllowedOpModel(LendApplication, '借入申请', borrow_request_perms),
    AllowedOpModel(BorrowingInReturnModel, '借入归还', borrowing_in_return_perms),
    AllowedOpModel(LoanApplicationOrder, '借出申请单', loan_application_perms),
    AllowedOpModel(LoanReturnOrder, '借出归还', loan_return_order_perms),
    AllowedOpModel(RepairApplication, '送修申请', repair_application_perms),
    AllowedOpModel(RepairReturnOrder, '送修归还', loan_return_order_perms),
    AllowedOpModel(AssembleApplication, '装机申请单', assemble_application_perms),
    AllowedOpModel(Assemble, '装机单', finish_perms),
    AllowedOpModel(ReturnMaterialOrder, '退料单', disassemble_order_perms),
    AllowedOpModel(DisassembleOrder, '拆机单', disassemble_order_perms),
    AllowedOpModel(Scrap, '报废单', scrap_perms),
    AllowedOpModel('expirewarning', '到期预警', expire_warning),
    AllowedOpModel('stockwarning', '库存预警', stock_warning),
    AllowedOpModel('checkwarning', '检查预警', check_warning),
]

model_allowed_perms = {}
for model in models:
    model_allowed_perms[model[0].encode('utf-8')] = \
        [item.encode('utf-8') for item in model[2]]


def get_model_display_name(model_name):
    for model in models:
        if model[0] == model_name:
            return model[1]
    return '未知'
