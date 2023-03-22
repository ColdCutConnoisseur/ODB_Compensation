import sys

from PyQt6.QtGui import QFont
from PyQt6.QtCore import QSize
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
                             QFrame,
                             QCheckBox)

from sales_people_crud import update_sales_people_table, return_sales_people_ids_and_names_as_dict
from sales_group_relationships_crud import (retrieve_group_relationship_by_sales_person,
                                            create_new_relationship,
                                            update_group_relationship,
                                            delete_group_relationship)
from jobs_crud import return_closed_jobs_count_for_employee

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

        gr_main_grid_layout.addWidget(group_lead_section_label, 2, 1)
        gr_main_grid_layout.addWidget(legacy_lead_section_label, 2, 3)

        current_group_lead_label = QLabel("Current Group Lead")
        self.gr_current_group_lead_text = QLineEdit(gui_config.DEFAULT_VALUE)
        self.gr_current_group_lead_text.setReadOnly(True)
        
        change_to_group_lead_label = QLabel("Change Group Lead To")
        self.gr_group_lead_dropdown = QComboBox()
        self.gr_group_lead_dropdown.addItems(self.names_list_w_na)

        gr_main_grid_layout.addWidget(current_group_lead_label, 3, 0)
        gr_main_grid_layout.addWidget(self.gr_current_group_lead_text, 3, 1)
        gr_main_grid_layout.addWidget(change_to_group_lead_label, 4, 0)
        gr_main_grid_layout.addWidget(self.gr_group_lead_dropdown, 4, 1)

        current_legacy_lead_label = QLabel("Current Legacy Lead")
        self.gr_current_legacy_lead_text = QLineEdit(gui_config.DEFAULT_VALUE)
        self.gr_current_legacy_lead_text.setReadOnly(True)

        change_to_legacy_lead_label = QLabel("Change Legacy Lead To")
        self.gr_legacy_group_lead_dropdown = QComboBox()
        self.gr_legacy_group_lead_dropdown.addItems(self.names_list_w_na)

        gr_main_grid_layout.addWidget(current_legacy_lead_label, 3, 2)
        gr_main_grid_layout.addWidget(self.gr_current_legacy_lead_text, 3, 3)
        gr_main_grid_layout.addWidget(change_to_legacy_lead_label, 4, 2)
        gr_main_grid_layout.addWidget(self.gr_legacy_group_lead_dropdown, 4, 3)

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

        gr_main_grid_layout.addWidget(self.create_relationship_button, 6, 1, 1, 2)
        gr_main_grid_layout.addWidget(self.update_relationship_button, 7, 1, 1, 2)
        gr_main_grid_layout.addWidget(self.delete_relationship_button, 8, 1, 1, 2)

        self.group_relationships_tab_widget.setLayout(gr_main_grid_layout)

    
    def setUp(self):
        update_sales_people_table()
        self.sales_people_and_ids_dict = return_sales_people_ids_and_names_as_dict()

        self.main_vertical_layout = QVBoxLayout()

        self.sales_person_select_h_layout = QHBoxLayout()

        sales_person_dropdown_label = QLabel("Sales Person")
        self.sales_person_dropdown_select = QComboBox()

        # Add Sales Person Names to dropdown
        sales_people = list(self.sales_people_and_ids_dict.keys())
        self.sales_person_dropdown_select.addItems(sales_people)

        self.sales_person_dropdown_select.currentIndexChanged.connect(self.on_main_page_sales_person_changed)

        self.sales_person_select_h_layout.addWidget(sales_person_dropdown_label)
        self.sales_person_select_h_layout.addWidget(self.sales_person_dropdown_select)

        self.group_relationships_summary_layout = QGridLayout()

        group_lead_label = QLabel("Group Lead")
        legacy_group_lead_label = QLabel("Legacy Group Lead")
        group_lead_job_count_label = QLabel("Group Lead Completed Jobs:")
        legacy_lead_job_count_label = QLabel("Legacy Lead Completed Jobs:")
        team_total_jobs_label = QLabel("Team Jobs Closed:")

        self.group_lead_name_text = QLineEdit()
        self.group_lead_name_text.setPlaceholderText(gui_config.DEFAULT_VALUE)
        self.group_lead_name_text.setReadOnly(True)

        self.legacy_group_lead_name_text = QLineEdit()
        self.legacy_group_lead_name_text.setPlaceholderText(gui_config.DEFAULT_VALUE)
        self.legacy_group_lead_name_text.setReadOnly(True)

        self.group_lead_job_count_text = QLineEdit()
        self.group_lead_job_count_text.setPlaceholderText(str(gui_config.ZERO_DEFAULT))
        self.group_lead_job_count_text.setReadOnly(True)

        self.legacy_group_lead_job_count_text = QLineEdit()
        self.legacy_group_lead_job_count_text.setPlaceholderText(str(gui_config.ZERO_DEFAULT))
        self.legacy_group_lead_job_count_text.setReadOnly(True)

        self.team_job_count_text = QLineEdit()
        self.team_job_count_text.setPlaceholderText(str(gui_config.ZERO_DEFAULT))
        self.team_job_count_text.setReadOnly(True)

        self.group_relationships_summary_layout.addWidget(group_lead_label, 0, 0)
        self.group_relationships_summary_layout.addWidget(self.group_lead_name_text, 0, 1)
        self.group_relationships_summary_layout.addWidget(group_lead_job_count_label, 0, 2)
        self.group_relationships_summary_layout.addWidget(self.group_lead_job_count_text, 0, 3)
        
        self.group_relationships_summary_layout.addWidget(legacy_group_lead_label, 1, 0)
        self.group_relationships_summary_layout.addWidget(self.legacy_group_lead_name_text, 1, 1)
        self.group_relationships_summary_layout.addWidget(legacy_lead_job_count_label, 1, 2)
        self.group_relationships_summary_layout.addWidget(self.legacy_group_lead_job_count_text, 1, 3)

        self.group_relationships_summary_layout.addWidget(team_total_jobs_label, 2, 2)
        self.group_relationships_summary_layout.addWidget(self.team_job_count_text, 2, 3)

        # Summary Data
        self.sales_person_summary_data_layout = QGridLayout()
        
        summary_header = QLabel("Summary")
        completed_jobs_label = QLabel("Num Completed Jobs:")
        self.completed_jobs_display = QLineEdit()
        self.completed_jobs_display.setReadOnly(True)
        self.completed_jobs_display.setPlaceholderText(str(gui_config.ZERO_DEFAULT))
        has_direct_recruit_label = QLabel("Has Direct Recruit(s)?")
        self.direct_recruit_checkbox = QCheckBox()
        self.direct_recruit_checkbox.setChecked(False)
        current_compensation_label = QLabel("Current Compensation Tier:")
        self.current_reward_tier_display = QLineEdit()
        self.current_reward_tier_display.setReadOnly(True)
        self.current_reward_tier_display.setPlaceholderText(spc.ProgramTiers.TIER_1A)

        self.sales_person_summary_data_layout.addWidget(summary_header, 0, 0, 1, 1)
        self.sales_person_summary_data_layout.addWidget(completed_jobs_label, 1, 3, 1, 1)
        self.sales_person_summary_data_layout.addWidget(self.completed_jobs_display, 1, 4, 1, 1)
        self.sales_person_summary_data_layout.addWidget(has_direct_recruit_label, 2, 3, 1, 1)
        self.sales_person_summary_data_layout.addWidget(self.direct_recruit_checkbox, 2, 4, 1, 1)
        self.sales_person_summary_data_layout.addWidget(current_compensation_label, 3, 3, 1, 1)
        self.sales_person_summary_data_layout.addWidget(self.current_reward_tier_display, 3, 4, 1, 1)

        # Nest Layouts
        self.main_vertical_layout.addLayout(self.sales_person_select_h_layout)
        self.main_vertical_layout.addLayout(self.sales_person_summary_data_layout)
        self.main_vertical_layout.addLayout(self.group_relationships_summary_layout)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_vertical_layout)

        #summary_frame = QFrame(self.main_widget)
        #summary_frame.setFrameShape(QFrame.StyledPanel)
        #summary_frame.setGeometry(200, 200, 200, 200)
        #summary_frame.setStyleSheet("background-color: white;")

        self.tab_widget = QTabWidget()
        # self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)
        self.tab_widget.addTab(self.main_widget, "Rewards Program Data")

        self.setUpGroupRelationshipsTab()

        self.tab_widget.addTab(self.group_relationships_tab_widget, "Edit Group Relationships")

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

        num_completed_jobs = return_closed_jobs_count_for_employee(self.database_name, sales_person_id)

        self.completed_jobs_display.setPlaceholderText(str(num_completed_jobs))

    def _update_group_lead_completed_jobs_count(self):
        current_group_lead_name = self.group_lead_name_text.placeholderText()
        
        if current_group_lead_name == gui_config.DEFAULT_VALUE:
            self.group_lead_job_count_text.setPlaceholderText(str(gui_config.ZERO_DEFAULT))

        else:
            group_lead_id = self._return_attributable_id_for_name(current_group_lead_name)
            group_lead_completed_jobs = return_closed_jobs_count_for_employee(self.database_name, group_lead_id)
            self.group_lead_job_count_text.setPlaceholderText(str(group_lead_completed_jobs))

    def _update_legacy_group_lead_completed_jobs_count(self):
        current_legacy_lead_name = self.legacy_group_lead_name_text.placeholderText()

        if current_legacy_lead_name == gui_config.DEFAULT_VALUE:
            self.legacy_group_lead_job_count_text.setPlaceholderText(str(gui_config.ZERO_DEFAULT))

        else:
            legacy_lead_id = self._return_attributable_id_for_name(current_legacy_lead_name)
            legacy_lead_completed_jobs = return_closed_jobs_count_for_employee(self.database_name, legacy_lead_id)
            self.legacy_group_lead_job_count_text.setPlaceholderText(str(legacy_lead_completed_jobs))

    def _update_team_closed_jobs_count(self):
        sales_person_job_count = int(self.completed_jobs_display.placeholderText())
        group_lead_job_count = int(self.group_lead_job_count_text.placeholderText())
        legacy_lead_job_count = int(self.legacy_group_lead_job_count_text.placeholderText())

        jobs_sum = sales_person_job_count + group_lead_job_count + legacy_lead_job_count

        self.team_job_count_text.setPlaceholderText(str(jobs_sum))

    def _calculate_and_update_current_program_tier(self):
        pass

    def _refresh_main_page(self):
        self._refresh_group_and_legacy_leads_displays_on_main_page()

        self._update_completed_jobs_count()

        self._update_group_lead_completed_jobs_count()

        self._update_legacy_group_lead_completed_jobs_count()

        self._update_team_closed_jobs_count()

        self._calculate_and_update_current_program_tier()


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

    def on_gr_sales_person_changed(self):
        print("Sales person changed!")
        self._refresh_group_and_legacy_leads_displays_on_relationships_page()
        
    def on_main_page_sales_person_changed(self):
        print("DEBUG: 'sales_person' changed on main tab")
        self._refresh_main_page()
        

app = QApplication(sys.argv)

DATABASE = spc.DB_NAME

window = CustomWindow(DATABASE)

# Start the event loop.
app.exec()