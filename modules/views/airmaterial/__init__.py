# coding:utf-8
# 工程技术范畴下的各模块视图定义

from .airmaterial_list import AirmaterialListView
from .in_bound import InBoundView
from .out_bound import OutBoundView
from .borrow_sheet import BorrowSheetView
from .claim_sheet import ClaimSheetView
from .install_sheet import InstallSheetView
from .lend_sheet import LendSheetView
from .purchase_contract import PurchaseContractView
from .repair_contract import RepairContractView
from .repair_supplier import RepairSupplierView
from .return_sheet import ReturnSheetView
from .supplier import SupplierView


__all__ = ['views']


views = [
    AirmaterialListView, InBoundView,
    OutBoundView, BorrowSheetView,
    ClaimSheetView, InstallSheetView,
    LendSheetView, PurchaseContractView,
    RepairContractView, RepairSupplierView,
    ReturnSheetView, SupplierView
]
