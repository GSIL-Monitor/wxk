# encoding: utf-8
from .storage import Storage, StorageList
from .airmaterial_list import AirmaterialList
from .disassemble_order import DisassembleOrder, DisassembleMaterial
from .lend_application import LendApplication, LendApplicationMaterial
from .purchase_application import PurchaseApplication, PurchaseMaterial
from .return_material_order import ReturnMaterialOrder, ReturnMaterial
from .airmaterial_category import AirmaterialCategory
from .borrowing_in_return import BorrowingInReturnModel, BorrowingInReturnMaterial
from .put_out_store import PutOutStoreModel, PutOutStoreMaterial
from .loan_application_order import LoanApplicationOrder, LoanMaterial
from .loan_return_order import LoanReturnOrder, LoanReturnMaterial
from .assemble import Assemble
from .assemble_application import AssembleApplication, AssembleApplicationList
from .repair_application import RepairApplication, RepairMaterial
from .manufacturer import Manufacturer
from .scrap import Scrap, ScrapMaterial
from .repair_return_order import RepairReturnOrder, RepairReturnMaterial
from .storage_list import AirMaterialStorageList
from .supplier import Supplier
from .repair_supplier import RepairSupplier


__all__ = [
    'Storage', 'AirmaterialList',
    'LendApplication', 'PurchaseApplication',
    'ReturnMaterialOrder', 'DisassembleOrder',
    'AirmaterialCategory', 'BorrowingInReturnModel',
    'AssembleApplication', 'PutOutStoreModel',
    'LoanReturnOrder', 'LoanApplicationOrder',
    'Assemble', 'RepairApplication', 'RepairMaterial',
    'Manufacturer', 'Scrap', 'LoanReturnMaterial',
    'RepairReturnOrder', 'RepairReturnMaterial',
    'DisassembleMaterial', 'AirMaterialStorageList',
    'PutOutStoreMaterial', 'Supplier', 'RepairSupplier',
    'AssembleApplicationList', 'BorrowingInReturnMaterial',
    'LendApplicationMaterial', 'LoanMaterial',
    'ReturnMaterial', 'ScrapMaterial', 'PurchaseMaterial',
    'StorageList']


views = [
    Storage, AirmaterialList,
    LendApplication, PurchaseApplication,
    ReturnMaterialOrder, DisassembleOrder,
    AirmaterialCategory, BorrowingInReturnModel,
    AssembleApplication, PutOutStoreModel,
    LoanReturnOrder, LoanApplicationOrder,
    Assemble, RepairApplication, RepairMaterial,
    Manufacturer, Scrap, LoanReturnMaterial,
    RepairReturnOrder, RepairReturnMaterial,
    DisassembleMaterial, AirMaterialStorageList,
    PutOutStoreMaterial, Supplier, RepairSupplier,
    AssembleApplicationList, BorrowingInReturnMaterial,
    LendApplicationMaterial, LoanMaterial,
    ReturnMaterial, ScrapMaterial,
    StorageList
]
