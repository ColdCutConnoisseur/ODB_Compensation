import sys

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
                             QPushButton)

from sales_people_crud import update_sales_people_table, return_sales_people_ids_and_names_as_dict
from sales_group_relationships_crud import retrieve_group_relationship_by_sales_person

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
        self.gr_main_vertical_layout = QVBoxLayout()

        self.gr_sales_person_select_and_display_layout = QHBoxLayout()

        gr_sales_person_dropdown_label = QLabel("Sales Person")
        self.gr_sales_person_dropdown_select = QComboBox()
        self.gr_sales_person_dropdown_select.currentIndexChanged.connect(self.on_gr_sales_person_changed)

        # Add Sales Person Names to dropdown
        sales_people = list(self.sales_people_and_ids_dict.keys())
        self.gr_sales_person_dropdown_select.addItems(sales_people)

        self.gr_sales_person_select_and_display_layout.addWidget(gr_sales_person_dropdown_label)
        self.gr_sales_person_select_and_display_layout.addWidget(self.gr_sales_person_dropdown_select)

        relationships_display_row = QHBoxLayout()

        group_lead_label = QLabel("Group Lead")
        self.gr_group_lead_dropdown = QComboBox()
        self.gr_group_lead_dropdown.addItems(self.names_list_w_na)

        legacy_lead_label = QLabel("Legacy Group Lead")
        self.gr_legacy_group_lead_dropdown = QComboBox()
        self.gr_legacy_group_lead_dropdown.addItems(self.names_list_w_na)

        relationships_display_row.addWidget(group_lead_label)
        relationships_display_row.addWidget(self.gr_group_lead_dropdown)
        relationships_display_row.addWidget(legacy_lead_label)
        relationships_display_row.addWidget(self.gr_legacy_group_lead_dropdown)

        create_h_layout = QHBoxLayout()
        update_h_layout = QHBoxLayout()
        delete_h_layout = QHBoxLayout()

        self.create_relationship_button = QPushButton("CREATE")
        self.update_relationship_button = QPushButton("UPDATE")
        self.delete_relationship_button = QPushButton("DELETE")

        # Signals --> Slots
        self.create_relationship_button.clicked.connect(self.create_relationship_button_clicked)
        self.update_relationship_button.clicked.connect(self.update_relationship_button_clicked)
        self.delete_relationship_button.clicked.connect(self.delete_relationship_button_clicked)

        create_h_layout.addWidget(self.create_relationship_button)
        update_h_layout.addWidget(self.update_relationship_button)
        delete_h_layout.addWidget(self.delete_relationship_button)

        self.gr_main_vertical_layout.addLayout(self.gr_sales_person_select_and_display_layout)
        self.gr_main_vertical_layout.addLayout(relationships_display_row)
        self.gr_main_vertical_layout.addLayout(create_h_layout)
        self.gr_main_vertical_layout.addLayout(update_h_layout)
        self.gr_main_vertical_layout.addLayout(delete_h_layout)

        self.group_relationships_tab_widget = QWidget(self)

        self.group_relationships_tab_widget.setLayout(self.gr_main_vertical_layout)



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

        self.sales_person_select_h_layout.addWidget(sales_person_dropdown_label)
        self.sales_person_select_h_layout.addWidget(self.sales_person_dropdown_select)

        self.group_relationships_summary_layout = QGridLayout()

        group_lead_label = QLabel("Group Lead")
        legacy_group_lead_label = QLabel("Legacy Group Lead")

        self.group_lead_name_text = QLineEdit()
        self.group_lead_name_text.setPlaceholderText(gui_config.DEFAULT_VALUE)

        self.legacy_group_lead_name_text = QLineEdit()
        self.legacy_group_lead_name_text.setPlaceholderText(gui_config.DEFAULT_VALUE)

        self.group_relationships_summary_layout.addWidget(group_lead_label, 0, 0)
        self.group_relationships_summary_layout.addWidget(self.group_lead_name_text, 0, 1)
        self.group_lead_name_text.setReadOnly(True)

        self.group_relationships_summary_layout.addWidget(legacy_group_lead_label, 1, 0)
        self.group_relationships_summary_layout.addWidget(self.legacy_group_lead_name_text, 1, 1)
        self.legacy_group_lead_name_text.setReadOnly(True)

        # Nest Layouts
        self.main_vertical_layout.addLayout(self.sales_person_select_h_layout)
        self.main_vertical_layout.addLayout(self.group_relationships_summary_layout)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_vertical_layout)

        self.tab_widget = QTabWidget()
        # self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)
        self.tab_widget.addTab(self.main_widget, "Sales Data")

        self.setUpGroupRelationshipsTab()

        self.tab_widget.addTab(self.group_relationships_tab_widget, "Edit Group Relationships")

        self.setCentralWidget(self.tab_widget)

        self._refresh_group_and_legacy_leads_displays()


    def _get_currently_selected_sales_person(self):
        currently_selected_sales_person = self.sales_person_dropdown_select.currentText()
        return currently_selected_sales_person

    def _return_attributable_id_for_name(self, sales_person_full_name):
        for k,v in self.sales_people_and_ids_dict.items():
            
            if k == sales_person_full_name:
                return v

    def _retrieve_group_and_legacy_leads_for_sales_person_id(self, sales_person_id):
        test_val = retrieve_group_relationship_by_sales_person(self.database_name, sales_person_id)
        return test_val

    def _set_group_lead_text(self, new_group_lead):
        self.group_lead_name_text.setPlaceholderText(new_group_lead)

    def _set_legacy_group_lead_text(self, new_legacy_lead):
        self.legacy_group_lead_name_text.setPlaceholderText(new_legacy_lead)

    def _refresh_group_and_legacy_leads_displays(self):
        current_sales_person = self._get_currently_selected_sales_person()

        attributable_id = self._return_attributable_id_for_name(current_sales_person)

        test_val = self._retrieve_group_and_legacy_leads_for_sales_person_id(attributable_id)

        if test_val is None:
            self._set_group_lead_text(gui_config.DEFAULT_VALUE)
            self._set_legacy_group_lead_text(gui_config.DEFAULT_VALUE)

        else:
            print("ADD LOGIC HERE!!!")


    def retrieve_and_set_group_relationship(self):
        pass






    # SLOTS
    def create_relationship_button_clicked(self):
        print("'Create' button clicked!")

    def update_relationship_button_clicked(self):
        print("'Update' button clicked!")

    def delete_relationship_button_clicked(self):
        print("'Delete' button clicked!")

    def on_gr_sales_person_changed(self):
        print("Sales person changed!")
        self.retrieve_and_set_group_relationship()
        


app = QApplication(sys.argv)

DATABASE = spc.DB_NAME

window = CustomWindow(DATABASE)

# Start the event loop.
app.exec()