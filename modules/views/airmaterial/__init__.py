# coding:utf-8
# 工程技术范畴下的各模块视图定义

from .airmaterial_list import AirmaterialListView
from .repair_supplier import RepairSupplierView
from .supplier import SupplierView
from .airmaterial_category import AirmaterialCategoryView
from .storage import StorageView
from .purchase_application import PurchaseApplicationView
from .lend_application import LendApplicationView
from .return_material_order import ReturnMaterialOrderView
from .disassemble_order import DisassembleOrderView
from .borrowing_in_return import BorrowingInReturnView
from .put_out_store import PutOutStoreView
from .assemble import AssembleView
from .assemble_application import AssembleApplicationView
from .loan_application_order import LoanApplicationOrderView
from .loan_return_order import LoanReturnOrderView
from .repair_application import RepairApplicationView
from .manufacturer import ManufacturerView
from .scrap import ScrapView
from .repair_return_order import RepairReturnOrderView
from .storage_list import AirMaterialStorageListView
from .check_waring import CheckWarningView
from .expire_warning import ExpireWarningView
from .stock_warning import StockWarningView

__all__ = ['views']


views = [
    AirmaterialListView, RepairSupplierView,
    SupplierView,
    AirmaterialCategoryView, StorageView,
    PurchaseApplicationView, AirMaterialStorageListView,
    LendApplicationView, ReturnMaterialOrderView,
    DisassembleOrderView, AssembleApplicationView,
    BorrowingInReturnView, AssembleView,
    PutOutStoreView, LoanReturnOrderView,
    LoanApplicationOrderView, RepairApplicationView,
    ManufacturerView, ScrapView, RepairReturnOrderView,
    CheckWarningView, ExpireWarningView, StockWarningView,
]
