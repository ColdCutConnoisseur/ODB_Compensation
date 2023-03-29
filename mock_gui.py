import sys
import time

from PyQt6.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt6.QtCore import QSize, QModelIndex
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QHBoxLayout,
                             QVBoxLayout,
                             QGridLayout,
                             QLabel,
                             QComboBox,
                             QLineEdit,
                             QTabWidget,
                             QPushButton,
                             QCheckBox,
                             QTreeView,
                             QListView)

from sales_people_crud import update_sales_people_table, return_sales_people_ids_and_names_as_dict
from sales_group_relationships_crud import (retrieve_group_relationship_by_sales_person,
                                            create_new_relationship,
                                            update_group_relationship,
                                            delete_group_relationship,
                                            fetch_all_people_one_level_down)
from sales_person_attribs_crud import (retrieve_attributes_record,
                                       create_or_update_attributes_record,
                                       return_contractor_has_direct_recruit)
from utility_functions import (fetch_current_job_count_for_contractor,
                               fetch_team_job_count,
                               calculate_reward_payouts_for_job)
from tier_classifier import revise_compensation_tier_based_on_overwrite
from jobs_crud import update_jobs_table, return_unprocessed_jobs

import sales_people_config as spc
import gui_config

class CustomWindow(QMainWindow):
    def __init__(self, database):
        super().__init__()

        self.database_name = database

        self.sales_people_and_ids_dict = {}

        self.setWindowTitle("ODB Compensation Calculator")
        self.setMinimumSize(QSize(900, 600))
        # .setMaximumSize()

        self.unprocessed_job_mapping = {}

        self.setUp()

        self.show()

    @property
    def names_list_w_na(self):
        names_list = list(self.sales_people_and_ids_dict.keys())
        names_list.insert(0, gui_config.DEFAULT_VALUE)
        return names_list

    def setUpGroupRelationshipsTab(self):
        self.group_relationships_tab_widget = QWidget(self)
        gr_main_grid_layout = QGridLayout()

        gr_sales_person_dropdown_label = QLabel("Sales Person")

        gr_main_grid_layout.addWidget(gr_sales_person_dropdown_label, 0, 0)

        self.gr_sales_person_dropdown_select = QComboBox()
        # Add Sales Person Names to dropdown
        sales_people = list(self.sales_people_and_ids_dict.keys())
        self.gr_sales_person_dropdown_select.addItems(sales_people)

        # signal --> slot
        self.gr_sales_person_dropdown_select.currentIndexChanged.connect(self.on_gr_sales_person_changed)

        gr_main_grid_layout.addWidget(self.gr_sales_person_dropdown_select, 0, 1)

        group_lead_section_label = QLabel("Group Lead")
        legacy_lead_section_label = QLabel("Legacy Group Lead")

        gr_main_grid_layout.addWidget(group_lead_section_label, 1, 1)
        gr_main_grid_layout.addWidget(legacy_lead_section_label, 1, 3)

        current_group_lead_label = QLabel("Current Group Lead")
        self.gr_current_group_lead_text = QLineEdit(gui_config.DEFAULT_VALUE)
        self.gr_current_group_lead_text.setReadOnly(True)
        
        change_to_group_lead_label = QLabel("Change Group Lead To")
        self.gr_group_lead_dropdown = QComboBox()
        self.gr_group_lead_dropdown.addItems(self.names_list_w_na)

        gr_main_grid_layout.addWidget(current_group_lead_label, 2, 0)
        gr_main_grid_layout.addWidget(self.gr_current_group_lead_text, 2, 1)
        gr_main_grid_layout.addWidget(change_to_group_lead_label, 3, 0)
        gr_main_grid_layout.addWidget(self.gr_group_lead_dropdown, 3, 1)

        current_legacy_lead_label = QLabel("Current Legacy Lead")
        self.gr_current_legacy_lead_text = QLineEdit(gui_config.DEFAULT_VALUE)
        self.gr_current_legacy_lead_text.setReadOnly(True)

        change_to_legacy_lead_label = QLabel("Change Legacy Lead To")
        self.gr_legacy_group_lead_dropdown = QComboBox()
        self.gr_legacy_group_lead_dropdown.addItems(self.names_list_w_na)

        gr_main_grid_layout.addWidget(current_legacy_lead_label, 2, 2)
        gr_main_grid_layout.addWidget(self.gr_current_legacy_lead_text, 2, 3)
        gr_main_grid_layout.addWidget(change_to_legacy_lead_label, 3, 2)
        gr_main_grid_layout.addWidget(self.gr_legacy_group_lead_dropdown, 3, 3)

        self.create_relationship_button = QPushButton("CREATE")
        self.update_relationship_button = QPushButton("UPDATE")
        self.delete_relationship_button = QPushButton("DELETE")

        # Default as disabled
        self.create_relationship_button.setEnabled(False)
        self.update_relationship_button.setEnabled(False)
        self.delete_relationship_button.setEnabled(False)

        # Signals --> Slots
        self.create_relationship_button.clicked.connect(self.create_relationship_button_clicked)
        self.update_relationship_button.clicked.connect(self.update_relationship_button_clicked)
        self.delete_relationship_button.clicked.connect(self.delete_relationship_button_clicked)

        gr_main_grid_layout.addWidget(self.create_relationship_button, 4, 3, 1, 1)
        gr_main_grid_layout.addWidget(self.update_relationship_button, 5, 3, 1, 1)
        gr_main_grid_layout.addWidget(self.delete_relationship_button, 6, 3, 1, 1)

        gr_main_grid_layout.setRowStretch(0, 10)
        gr_main_grid_layout.setRowStretch(1, 0)


        self.group_relationships_tab_widget.setLayout(gr_main_grid_layout)

    def setUpSalesPersonAttribsTab(self):
        self.sales_person_attribs_tab_widget = QWidget(self)

        sp_main_grid_layout = QGridLayout()

        sp_sales_person_dropdown_label = QLabel("Sales Person")

        self.sp_sales_person_dropdown_select = QComboBox()
        # Add Sales Person Names to dropdown
        sales_people = list(self.sales_people_and_ids_dict.keys())
        self.sp_sales_person_dropdown_select.addItems(sales_people)

        self.sp_sales_person_dropdown_select.currentIndexChanged.connect(self.on_sp_sales_person_changed)

        initial_job_count_label = QLabel("Initial Job Count")

        self.sp_initial_job_count_display = QLineEdit()
        self.sp_initial_job_count_display.setText(str(gui_config.ZERO_DEFAULT))

        has_recruit_attrib_label = QLabel("Has Recruit(s)?")
        self.sp_has_recruit_checkbox = QCheckBox()
        self.sp_has_recruit_checkbox.setChecked(False)

        tier_overwrite_label = QLabel("Rewards Program Tier Overwrite")

        self.sp_tier_overwrite_dropdown = QComboBox()
        tier_options = spc.ProgramTiers.TIER_OPTIONS
        self.sp_tier_overwrite_dropdown.addItems(tier_options)

        self.sp_tier_overwrite_display = QLineEdit()
        self.sp_tier_overwrite_display.setReadOnly(True)
        self.sp_tier_overwrite_display.setText(gui_config.DEFAULT_VALUE)

        tier_overwrite_change_label = QLabel("Change Tier To")

        self.sp_update_person_attributes_button = QPushButton("Create / Update")

        self.sp_update_person_attributes_button.clicked.connect(self.on_sp_update_clicked)

        sp_main_grid_layout.addWidget(sp_sales_person_dropdown_label, 0, 0)
        sp_main_grid_layout.addWidget(self.sp_sales_person_dropdown_select, 0, 1)

        sp_main_grid_layout.addWidget(initial_job_count_label, 1, 0)
        sp_main_grid_layout.addWidget(self.sp_initial_job_count_display, 1, 1)

        sp_main_grid_layout.addWidget(has_recruit_attrib_label, 2, 0)
        sp_main_grid_layout.addWidget(self.sp_has_recruit_checkbox, 2, 1)

        sp_main_grid_layout.addWidget(tier_overwrite_label, 3, 0)
        sp_main_grid_layout.addWidget(self.sp_tier_overwrite_display, 3, 1)
        sp_main_grid_layout.addWidget(tier_overwrite_change_label, 3, 2)
        sp_main_grid_layout.addWidget(self.sp_tier_overwrite_dropdown, 3, 3)

        sp_main_grid_layout.addWidget(self.sp_update_person_attributes_button, 4, 0, 1, 4)

        self.sales_person_attribs_tab_widget.setLayout(sp_main_grid_layout)

        self._refresh_person_attributes_page()

    def setUpOrgChartTab(self):
        self.org_tab_widget = QWidget(self)

        self.org_sales_person_dropdown_select = QComboBox()
        # Add Sales Person Names to dropdown
        sales_people = list(self.sales_people_and_ids_dict.keys())
        self.org_sales_person_dropdown_select.addItems(sales_people)

        self.org_sales_person_dropdown_select.currentIndexChanged.connect(self.on_refresh_org_chart)

        org_main_vertical_layout = QVBoxLayout()

        dropdown_h_layout = QHBoxLayout()

        self.tree_layout = QHBoxLayout()

        self.org_tree = QTreeView()
        self.org_tree.setHeaderHidden(False)

        self.tree_layout.addWidget(self.org_tree)

        dropdown_h_layout.addWidget(self.org_sales_person_dropdown_select)

        org_main_vertical_layout.addLayout(dropdown_h_layout)
        org_main_vertical_layout.addLayout(self.tree_layout)

        self.org_tab_widget.setLayout(org_main_vertical_layout)

        self.on_refresh_org_chart()

    def setUp(self):
        update_sales_people_table()
        update_jobs_table(self.database_name)

        self.sales_people_and_ids_dict = return_sales_people_ids_and_names_as_dict()

        self.main_grid_layout = QGridLayout()

        sales_person_dropdown_label = QLabel("Sales Person")
        self.sales_person_dropdown_select = QComboBox()

        # Add Sales Person Names to dropdown
        sales_people = list(self.sales_people_and_ids_dict.keys())
        self.sales_person_dropdown_select.addItems(sales_people)

        self.sales_person_dropdown_select.currentIndexChanged.connect(self.on_main_page_sales_person_changed)

        # Summary Data
        summary_header = QLabel("Summary")
        completed_jobs_label = QLabel("Num Completed Jobs:")
        self.completed_jobs_display = QLineEdit()
        self.completed_jobs_display.setReadOnly(True)
        self.completed_jobs_display.setPlaceholderText(str(gui_config.ZERO_DEFAULT))
        has_direct_recruit_label = QLabel("Has Direct Recruit(s)?")
        self.direct_recruit_checkbox = QCheckBox()
        self.direct_recruit_checkbox.setChecked(False)
        team_total_jobs_label = QLabel("Team Jobs Closed:")
        self.team_job_count_text = QLineEdit()
        self.team_job_count_text.setPlaceholderText(str(gui_config.ZERO_DEFAULT))
        self.team_job_count_text.setReadOnly(True)
        current_compensation_label = QLabel("Current Compensation Tier:")
        self.current_reward_tier_display = QLineEdit()
        self.current_reward_tier_display.setReadOnly(True)
        self.current_reward_tier_display.setPlaceholderText(spc.ProgramTiers.TIER_1A)

        group_lead_label = QLabel("Group Lead")
        legacy_group_lead_label = QLabel("Legacy Group Lead")
        self.group_lead_name_text = QLineEdit()
        self.group_lead_name_text.setPlaceholderText(gui_config.DEFAULT_VALUE)
        self.group_lead_name_text.setReadOnly(True)
        self.legacy_group_lead_name_text = QLineEdit()
        self.legacy_group_lead_name_text.setPlaceholderText(gui_config.DEFAULT_VALUE)
        self.legacy_group_lead_name_text.setReadOnly(True)

        unprocessed_jobs_label = QLabel("Unprocessed Jobs")
        self.unprocessed_jobs_list = QComboBox()

        self.unprocessed_jobs_list.currentIndexChanged.connect(self.on_unprocessed_jobs_selection_change)
        #self.unprocessed_jobs_list = QListView()
        #self.unprocessed_jobs_model = QStandardItemModel()
        #self.unprocessed_jobs_list.setModel(self.unprocessed_jobs_model)
        #self.unprocessed_jobs_list.clicked[QModelIndex].connect(self.on_up_jobs_list_clicked)

        gross_profit_label = QLabel("Gross Profit")
        self.gross_profit_amount = QLineEdit()

        self.gross_profit_amount.textChanged.connect(self.on_gross_profit_text_changed)

        job_eligible_label = QLabel("Job Eligible For Program?")
        self.job_eligible_checkbox = QCheckBox()
        self.job_eligible_checkbox.stateChanged.connect(self.on_job_eligibility_changed)

        group_lead_payable_label = QLabel("Payable -- Group Lead")
        self.group_lead_payable_amount = QLineEdit()
        self.group_lead_payable_amount.setReadOnly(True)
        self.group_lead_payable_amount.setText(str(gui_config.ZERO_DEFAULT))

        legacy_lead_payable_label = QLabel("Payable -- Legacy Lead")
        self.legacy_lead_payable_amount = QLineEdit()
        self.legacy_lead_payable_amount.setReadOnly(True)
        self.legacy_lead_payable_amount.setText(str(gui_config.ZERO_DEFAULT))

        self.main_grid_layout.addWidget(sales_person_dropdown_label, 0, 0)
        self.main_grid_layout.addWidget(self.sales_person_dropdown_select, 0, 1, 1, 2)
        self.main_grid_layout.addWidget(unprocessed_jobs_label, 1, 0)
        self.main_grid_layout.addWidget(self.unprocessed_jobs_list, 1, 1)
        self.main_grid_layout.addWidget(gross_profit_label, 2, 1)
        self.main_grid_layout.addWidget(self.gross_profit_amount, 2, 2)
        self.main_grid_layout.addWidget(job_eligible_label, 3, 1)
        self.main_grid_layout.addWidget(self.job_eligible_checkbox, 3, 2)
        self.main_grid_layout.addWidget(summary_header, 6, 0)
        self.main_grid_layout.addWidget(completed_jobs_label, 7, 1)
        self.main_grid_layout.addWidget(self.completed_jobs_display, 7, 2)
        self.main_grid_layout.addWidget(has_direct_recruit_label, 8, 1)
        self.main_grid_layout.addWidget(self.direct_recruit_checkbox, 8, 2)
        self.main_grid_layout.addWidget(team_total_jobs_label, 9, 1)
        self.main_grid_layout.addWidget(self.team_job_count_text, 9, 2)
        self.main_grid_layout.addWidget(current_compensation_label, 10, 1)
        self.main_grid_layout.addWidget(self.current_reward_tier_display, 10, 2)
        self.main_grid_layout.addWidget(group_lead_label, 11, 1)
        self.main_grid_layout.addWidget(self.group_lead_name_text, 11, 2)
        self.main_grid_layout.addWidget(legacy_group_lead_label, 12, 1)
        self.main_grid_layout.addWidget(self.legacy_group_lead_name_text, 12, 2)

        self.main_grid_layout.addWidget(group_lead_payable_label, 13, 1)
        self.main_grid_layout.addWidget(self.group_lead_payable_amount, 13, 2)
        self.main_grid_layout.addWidget(legacy_lead_payable_label, 14, 1)
        self.main_grid_layout.addWidget(self.legacy_lead_payable_amount, 14, 2)
        
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_grid_layout)

        self.tab_widget = QTabWidget()
        # self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)
        self.tab_widget.addTab(self.main_widget, "Rewards Calculator")

        self.setUpGroupRelationshipsTab()
        self.setUpSalesPersonAttribsTab()
        self.setUpOrgChartTab()

        self.tab_widget.addTab(self.group_relationships_tab_widget, "Edit Group Relationships")
        self.tab_widget.addTab(self.sales_person_attribs_tab_widget, "Edit Sales Person Attributes")
        self.tab_widget.addTab(self.org_tab_widget, "Org Chart")

        self.setCentralWidget(self.tab_widget)

        self._refresh_group_and_legacy_leads_displays_on_relationships_page()

        self._refresh_main_page()


    def _get_currently_selected_sales_person_main_page(self):
        currently_selected_sales_person = self.sales_person_dropdown_select.currentText()
        return currently_selected_sales_person

    def _get_currently_selected_sales_person_relationships_page(self):
        currently_selected_sales_person = self.gr_sales_person_dropdown_select.currentText()
        return currently_selected_sales_person

    def _return_attributable_id_for_name(self, sales_person_full_name):
        for k,v in self.sales_people_and_ids_dict.items():
            
            if k == sales_person_full_name:
                return v

    def _return_attributable_name_for_id(self, contractor_id):
        for k,v in self.sales_people_and_ids_dict.items():

            if v == contractor_id:
                return k

    def _retrieve_group_and_legacy_leads_for_sales_person_id(self, sales_person_id):
        test_val = retrieve_group_relationship_by_sales_person(self.database_name, sales_person_id)
        return test_val

    def _set_group_lead_text_main_page(self, new_group_lead):
        self.group_lead_name_text.setPlaceholderText(new_group_lead)

    def _set_legacy_group_lead_text_main_page(self, new_legacy_lead):
        self.legacy_group_lead_name_text.setPlaceholderText(new_legacy_lead)

    def _refresh_group_and_legacy_leads_displays_on_main_page(self):
        current_sales_person = self._get_currently_selected_sales_person_main_page()

        attributable_id = self._return_attributable_id_for_name(current_sales_person)

        fetched_relationship = self._retrieve_group_and_legacy_leads_for_sales_person_id(attributable_id)

        # If 'id' doesn't exist in the database table
        if fetched_relationship is None:
            self._set_group_lead_text_main_page(gui_config.DEFAULT_VALUE)
            self._set_legacy_group_lead_text_main_page(gui_config.DEFAULT_VALUE)

        else:
            # If exists, fetched_relationship will be tuple of three values

            as_list_repr = list(fetched_relationship)

            retrieved_group_id = as_list_repr[1]
            retrieved_legacy_id = as_list_repr[2]

            if retrieved_group_id is None:
                self._set_group_lead_text_main_page(gui_config.DEFAULT_VALUE)

            elif retrieved_group_id is not None:
                c_name = self._return_attributable_name_for_id(retrieved_group_id)
                self._set_group_lead_text_main_page(c_name)

            if retrieved_legacy_id is None:
                self._set_legacy_group_lead_text_main_page(gui_config.DEFAULT_VALUE)

            elif retrieved_legacy_id is not None:
                c_name = self._return_attributable_name_for_id(retrieved_legacy_id)
                self._set_legacy_group_lead_text_main_page(c_name)

    def _set_group_lead_text_relationships_page(self, new_group_lead):
        self.gr_current_group_lead_text.setText(new_group_lead)

    def _set_legacy_group_lead_text_relationships_page(self, new_legacy_lead):
        self.gr_current_legacy_lead_text.setText(new_legacy_lead)

    def _refresh_group_and_legacy_leads_displays_on_relationships_page(self):
        current_sales_person = self._get_currently_selected_sales_person_relationships_page()

        attributable_id = self._return_attributable_id_for_name(current_sales_person)

        fetched_relationship = self._retrieve_group_and_legacy_leads_for_sales_person_id(attributable_id)

        # If 'id' doesn't exist in the database table
        if fetched_relationship is None:
            self._set_group_lead_text_relationships_page(gui_config.DEFAULT_VALUE)
            self._set_legacy_group_lead_text_relationships_page(gui_config.DEFAULT_VALUE)

            # Only enable 'Create' button
            self.create_relationship_button.setEnabled(True)
            self.update_relationship_button.setEnabled(False)
            self.delete_relationship_button.setEnabled(False)
            
        else:
            # If exists, fetched_relationship will be tuple of three values
            print(fetched_relationship)

            as_list_repr = list(fetched_relationship)

            retrieved_group_id = as_list_repr[1]
            retrieved_legacy_id = as_list_repr[2]

            if retrieved_group_id is None:
                self._set_group_lead_text_relationships_page(gui_config.DEFAULT_VALUE)

            elif retrieved_group_id is not None:
                c_name = self._return_attributable_name_for_id(retrieved_group_id)
                self._set_group_lead_text_relationships_page(c_name)

            if retrieved_legacy_id is None:
                self._set_legacy_group_lead_text_relationships_page(gui_config.DEFAULT_VALUE)

            elif retrieved_legacy_id is not None:
                c_name = self._return_attributable_name_for_id(retrieved_legacy_id)
                self._set_legacy_group_lead_text_relationships_page(c_name)

            # Disable 'Create' button if relationship exists
            self.create_relationship_button.setEnabled(False)
            self.update_relationship_button.setEnabled(True)
            self.delete_relationship_button.setEnabled(True)

    def _update_completed_jobs_count(self):
        current_sales_person = self._get_currently_selected_sales_person_main_page()

        sales_person_id = self._return_attributable_id_for_name(current_sales_person)

        num_completed_jobs = fetch_current_job_count_for_contractor(self.database_name, sales_person_id)

        self.completed_jobs_display.setText(str(num_completed_jobs))

        return num_completed_jobs

    def _update_team_closed_jobs_count(self):
        current_sales_person = self._get_currently_selected_sales_person_main_page()

        sales_person_id = self._return_attributable_id_for_name(current_sales_person)

        team_job_count = fetch_team_job_count(self.database_name, sales_person_id)

        self.team_job_count_text.setPlaceholderText(str(team_job_count))

        return team_job_count

    def _update_direct_recruit_checkbox(self):
        current_sales_person = self._get_currently_selected_sales_person_main_page()

        sales_person_id = self._return_attributable_id_for_name(current_sales_person)

        has_direct_recruit = return_contractor_has_direct_recruit(self.database_name, sales_person_id)

        # Update checkbox
        self.direct_recruit_checkbox.setChecked(has_direct_recruit)

        return has_direct_recruit

    def _calculate_and_update_current_program_tier(self, num_closed_contractor_jobs, num_closed_team_jobs,
            has_direct_recruit):
        current_sales_person = self._get_currently_selected_sales_person_main_page()

        sales_person_id = self._return_attributable_id_for_name(current_sales_person)

        abs_tier = revise_compensation_tier_based_on_overwrite(
                            self.database_name,
                            sales_person_id,
                            num_closed_contractor_jobs,
                            num_closed_team_jobs,
                            has_direct_recruit)

        self.current_reward_tier_display.setPlaceholderText(abs_tier)

    def _update_unprocessed_jobs_list(self):
        # update_jobs_table(self.database_name)
        unprocessed_jobs = return_unprocessed_jobs(self.database_name)

        self.unprocessed_job_mapping.clear()
        self.unprocessed_job_mapping = {up_job[0] : up_job[1] for up_job in unprocessed_jobs}

        jobs_as_strings = [str(j_num) for j_num in self.unprocessed_job_mapping.keys()]

        self.unprocessed_jobs_list.clear()
        self.unprocessed_jobs_list.addItems(jobs_as_strings)

    def _refresh_main_page(self):
        self._update_unprocessed_jobs_list()

        # Automatically switch to sales_person for first unhandled_job
        if len(list(self.unprocessed_job_mapping.keys())) > 0:
            # Change index for sales person
            current_job_num = int(self.unprocessed_jobs_list.currentText())

            job_sales_person_id = self.unprocessed_job_mapping[current_job_num]

            select_index = 0

            for ct, sales_person_id in enumerate(self.sales_people_and_ids_dict.values()):
                if sales_person_id == job_sales_person_id:
                    select_index = ct
                    break

            self.sales_person_dropdown_select.setCurrentIndex(select_index)

        self._refresh_group_and_legacy_leads_displays_on_main_page()

        num_completed_jobs = self._update_completed_jobs_count()

        num_team_jobs = self._update_team_closed_jobs_count()

        has_direct_recruit = self._update_direct_recruit_checkbox()

        self._calculate_and_update_current_program_tier(num_completed_jobs, num_team_jobs, has_direct_recruit)

    def _sp_set_default_values_for_all_widgets(self):
        self.sp_initial_job_count_display.setText(str(gui_config.ZERO_DEFAULT))
        self.sp_has_recruit_checkbox.setChecked(False)
        self.sp_tier_overwrite_display.setText(gui_config.DEFAULT_VALUE)

    def _update_initial_job_count_display_attribs_tab(self, initial_jobs_count):
        self.sp_initial_job_count_display.setText(str(initial_jobs_count))

    def _update_has_recruits_display_attribs_tab(self, has_recruit_attrib):
        self.sp_has_recruit_checkbox.setChecked(has_recruit_attrib)

    def _update_rewards_tier_overwrite_attribs_tab(self, rewards_tier):
        if rewards_tier is None:
            self.sp_tier_overwrite_display.setText(gui_config.DEFAULT_VALUE)
        
        else:
            self.sp_tier_overwrite_display.setText(rewards_tier)

    def _refresh_person_attributes_page(self):
        currently_selected_sales_person_name = self.sp_sales_person_dropdown_select.currentText()

        sales_person_id =\
            self._return_attributable_id_for_name(currently_selected_sales_person_name)

        attribs_record = retrieve_attributes_record(self.database_name, sales_person_id)

        if attribs_record is None:
            self._sp_set_default_values_for_all_widgets()

        else:
            print(attribs_record)

            as_list = list(attribs_record)

            initial_jobs_count = as_list[1]
            has_recruit_attrib = as_list[2]
            rewards_tier = as_list[3]

            self._update_initial_job_count_display_attribs_tab(initial_jobs_count)
            self._update_has_recruits_display_attribs_tab(has_recruit_attrib)
            self._update_rewards_tier_overwrite_attribs_tab(rewards_tier)



    # SLOTS
    def create_relationship_button_clicked(self):
        print("'Create' button clicked!")

        # Get Values (names)
        sales_person_name = self._get_currently_selected_sales_person_relationships_page()
        group_lead_name = self.gr_group_lead_dropdown.currentText()
        legacy_lead_name = self.gr_legacy_group_lead_dropdown.currentText()

        # Translate names to IDs
        sales_person_id = self._return_attributable_id_for_name(sales_person_name)
        group_lead_id = self._return_attributable_id_for_name(group_lead_name)
        legacy_lead_id = self._return_attributable_id_for_name(legacy_lead_name)

        print(f"Sales: {sales_person_id}")
        print(f"Group: {group_lead_id}")
        print(f"Legacy {legacy_lead_id}")

        try:
            create_new_relationship(self.database_name, sales_person_id, group_lead_id, legacy_lead_id)
            self._refresh_group_and_legacy_leads_displays_on_relationships_page()

        except:
            pass

    def update_relationship_button_clicked(self):
        print("'Update' button clicked!")

        # Get Values (names)  #TODO: Refector -- codeblock also present in 'create' method
        sales_person_name = self._get_currently_selected_sales_person_relationships_page()
        group_lead_name = self.gr_group_lead_dropdown.currentText()
        legacy_lead_name = self.gr_legacy_group_lead_dropdown.currentText()

        # Translate names to IDs
        sales_person_id = self._return_attributable_id_for_name(sales_person_name)
        group_lead_id = self._return_attributable_id_for_name(group_lead_name)
        legacy_lead_id = self._return_attributable_id_for_name(legacy_lead_name)

        print(f"Sales: {sales_person_id}")
        print(f"Group: {group_lead_id}")
        print(f"Legacy {legacy_lead_id}")

        update_group_relationship(self.database_name, sales_person_id, group_lead_id, legacy_lead_id)

        self._refresh_group_and_legacy_leads_displays_on_relationships_page()

    def delete_relationship_button_clicked(self):
        print("'Delete' button clicked!")

        sales_person_name = self._get_currently_selected_sales_person_relationships_page()
        sales_person_id = self._return_attributable_id_for_name(sales_person_name)
        delete_group_relationship(self.database_name, sales_person_id)

        self._refresh_group_and_legacy_leads_displays_on_relationships_page()

    def on_sp_sales_person_changed(self):
        self._refresh_person_attributes_page()

    def on_gr_sales_person_changed(self):
        print("Sales person changed!")
        self._refresh_group_and_legacy_leads_displays_on_relationships_page()
        
    def on_main_page_sales_person_changed(self):
        self._refresh_main_page()
        
    def on_refresh_org_chart(self):
        currently_selected_name = self.org_sales_person_dropdown_select.currentText()

        sales_person_id = self._return_attributable_id_for_name(currently_selected_name)

        children = fetch_all_people_one_level_down(self.database_name, sales_person_id)

        tree_model = QStandardItemModel()
        root_node = tree_model.invisibleRootItem()

        parent_sales_person_name = QStandardItem(currently_selected_name)
        parent_ind_jobs_count = fetch_current_job_count_for_contractor(self.database_name, sales_person_id)
        parent_team_jobs_count = fetch_team_job_count(self.database_name, sales_person_id)
        parent_has_recruit = return_contractor_has_direct_recruit(self.database_name, sales_person_id)
        parent_current_tier = revise_compensation_tier_based_on_overwrite(self.database_name, sales_person_id,
                                                        parent_ind_jobs_count, parent_team_jobs_count,
                                                        parent_has_recruit)

        root_row = [parent_sales_person_name,
                    QStandardItem(str(parent_ind_jobs_count)),
                    QStandardItem(str(parent_team_jobs_count)),
                    QStandardItem(parent_current_tier)]

        root_node.appendRow(root_row)
        
        for child in children:
            t_name = self._return_attributable_name_for_id(child)

            individual_job_count = fetch_current_job_count_for_contractor(self.database_name, child)
            team_job_count = fetch_team_job_count(self.database_name, child)
            has_direct_recruit = return_contractor_has_direct_recruit(self.database_name, child)

            current_tier = revise_compensation_tier_based_on_overwrite(self.database_name, child,
                                                        individual_job_count, team_job_count,
                                                        has_direct_recruit)
            
            new_item = QStandardItem(t_name)
            job_count = QStandardItem(str(individual_job_count))
            team_jobs = QStandardItem(str(team_job_count))
            tier = QStandardItem(current_tier)

            child_row = [new_item, job_count, team_jobs, tier]

            parent_sales_person_name.appendRow(child_row)

            grandchildren = fetch_all_people_one_level_down(self.database_name, child)

            for gc in grandchildren:
                gc_name = self._return_attributable_name_for_id(gc)

                gc_job_count_fetch = fetch_current_job_count_for_contractor(self.database_name, gc)
                gc_team_job_count_fetch = fetch_team_job_count(self.database_name, gc)
                gc_has_recruit_fetch = return_contractor_has_direct_recruit(self.database_name, gc)

                gc_current_tier = revise_compensation_tier_based_on_overwrite(self.database_name, gc,
                                                            gc_job_count_fetch, gc_team_job_count_fetch,
                                                            gc_has_recruit_fetch)

                gc_item = QStandardItem(gc_name)
                gc_job_count = QStandardItem(str(gc_job_count_fetch))
                gc_team_job_count = QStandardItem(str(gc_team_job_count_fetch))
                gc_tier = QStandardItem(gc_current_tier)

                new_item.appendRow([gc_item, gc_job_count, gc_team_job_count, gc_tier])

        self.org_tree.setModel(tree_model)
        self.org_tree.expandAll()
        self.org_tree.setColumnWidth(0, 400)

    def on_sp_update_clicked(self):
        current_sales_person_name = self.sp_sales_person_dropdown_select.currentText()

        sales_person_id = self._return_attributable_id_for_name(current_sales_person_name)

        new_job_count = int(self.sp_initial_job_count_display.text())

        recruit_update = self.sp_has_recruit_checkbox.isChecked()

        tier_ow = self.sp_tier_overwrite_dropdown.currentText()

        if tier_ow == gui_config.DEFAULT_VALUE:
            tier_ow = None

        create_or_update_attributes_record(self.database_name, sales_person_id,
            initial_job_count=new_job_count, has_recruit=recruit_update, rewards_tier_overwrite=tier_ow)

        self._refresh_person_attributes_page()

    def DEPRon_up_jobs_list_clicked(self, click_index):
        job_num_object = self.unprocessed_jobs_model.itemFromIndex(click_index)
        job_num = job_num_object.text()

        associated_contractor_id = self.unprocessed_job_mapping[int(job_num)]

        print(associated_contractor_id)

        self.sales_person_dropdown_select.setCurrentIndex(5)

    def on_unprocessed_jobs_selection_change(self):
        print(self.unprocessed_jobs_list.currentText())

    def on_gross_profit_text_changed(self):
        job_gross_profit = self.gross_profit_amount.text()

        # Check for empty 'gross profit'
        if job_gross_profit == '':
            print("job_gross_profit is empty")
            print(0, 0)

        else:
            is_job_eligible = self.job_eligible_checkbox.isChecked()

            current_group_lead_name = self.group_lead_name_text.text()
            current_legacy_lead_name = self.legacy_group_lead_name_text.text()

            # Translate 'N/A' values to None type
            if current_group_lead_name == gui_config.DEFAULT_VALUE:
                current_group_lead_name = None

            if current_legacy_lead_name == gui_config.DEFAULT_VALUE:
                current_legacy_lead_name = None

            group_lead_id = None
            legacy_lead_id = None

            if current_group_lead_name is not None:
                group_lead_id = self._return_attributable_id_for_name(current_group_lead_name)
            
            if current_legacy_lead_name is not None:
                legacy_lead_id = self._return_attributable_id_for_name(current_legacy_lead_name)

            group_lead_payout, legacy_lead_payout = calculate_reward_payouts_for_job(
                                                        is_job_eligible,
                                                        self.database_name,
                                                        group_lead_id,
                                                        legacy_lead_id,
                                                        job_gross_profit
            )

            print(group_lead_payout, legacy_lead_payout)

    def on_job_eligibility_changed(self):
        self.on_gross_profit_text_changed()

app = QApplication(sys.argv)

DATABASE = spc.DB_NAME

window = CustomWindow(DATABASE)

# Start the event loop
app.exec()