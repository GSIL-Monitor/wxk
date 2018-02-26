# encoding: utf-8

from __future__ import unicode_literals


__all__ = [
    'PurchaseSTORE', 'LendSTORE', 'ReturnMaterialSTORE',
    'DisassembleSTORE', 'RepairReturnSTORE', 'LoanReturnSTORE',
    'purchaseStore', 'lendStore', 'retrunMaterialStore',
    'disassembleStore', 'repairReturnStore', 'loanReturnStore',
    'LoanOutSTORE', 'BorrowReturnOutSTORE', 'AssembleOutSTORE',
    'RepairOutSTORE', 'ScrapOutSTORE', 'loanOutstore',
    'borrowReturnOutStore', 'assembleOutStore', 'repairOutStore',
    'scrapOutStore']


# 入库
PurchaseSTORE = '采购入库'

LendSTORE = '借入入库'

ReturnMaterialSTORE = '退料入库'

DisassembleSTORE = '拆机入库'

RepairReturnSTORE = '送修归还入库'

LoanReturnSTORE = '借出归还入库'

purchaseStore = 'purchase'

lendStore = 'lend'

retrunMaterialStore = 'return_material'

disassembleStore = 'disassemble'

repairReturnStore = 'repair_return'

loanReturnStore = 'loan_return'

# 出库
LoanOutSTORE = '借出出库'

BorrowReturnOutSTORE = '借入归还出库'

AssembleOutSTORE = '装机出库'

RepairOutSTORE = '送修出库'

ScrapOutSTORE = '报废出库'

loanOutstore = 'loan_outstore'

borrowReturnOutStore = 'borrow_return_outstore'

assembleOutStore = 'assemble_outstore'

repairOutStore = 'repair_outstore'

scrapOutStore = 'scrap_outstore'
