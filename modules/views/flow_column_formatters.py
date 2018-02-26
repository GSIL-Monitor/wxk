# coding: utf-8

from __future__ import unicode_literals

from .operations import group_operation_formatter

from column_formatter import reviewing_user_name_formater
from column_formatter import creat_information_formater
from column_formatter import creat_information_formater
from column_formatter import amend_information_formater
from column_formatter import amend_information_formater
from column_formatter import reviewing_user_name_formater
from column_formatter import review_information_formater
from column_formatter import review_information_formater
from column_formatter import review_information_formater
from column_formatter import approving_user_name_formater
from column_formatter import approved_information_formater
from column_formatter import approved_information_formater
from column_formatter import approved_information_formater
from column_formatter import commit_information_formater
from column_formatter import commit_information_formater
from column_formatter import sec_approving_user_name_formater
from column_formatter import sec_approved_information_formater
from column_formatter import sec_approved_information_formater
from column_formatter import sec_approved_information_formater
from column_formatter import sent_information_formater
from column_formatter import sent_information_formater
from column_formatter import receive_information_formater
from column_formatter import receive_information_formater
from column_formatter import receiving_user_information_formater


flow_column_formatters = {
    'groupOperation': group_operation_formatter,
    'reviewingUser': reviewing_user_name_formater,
    'createUserName': creat_information_formater,
    'createTime': creat_information_formater,
    'amendUserName': amend_information_formater,
    'amendTime': amend_information_formater,
    'reviewingUser': reviewing_user_name_formater,
    'reviewUserName': review_information_formater,
    'reviewTime': review_information_formater,
    'reviewSuggestions': review_information_formater,
    'approvingUser': approving_user_name_formater,
    'approveUserName': approved_information_formater,
    'approveTime': approved_information_formater,
    'approveSuggestions': approved_information_formater,
    'commitUserName': commit_information_formater,
    'commitTime': commit_information_formater,
    'secApprovingUser': sec_approving_user_name_formater,
    'secApproveUserName': sec_approved_information_formater,
    'secApproveTime': sec_approved_information_formater,
    'secApproveSuggestions': sec_approved_information_formater,
    'sentPerson': sent_information_formater,
    'sentTime': sent_information_formater,
    'receivePerson': receive_information_formater,
    'receiveTime': receive_information_formater,
    'receivingUser': receiving_user_information_formater,
}
