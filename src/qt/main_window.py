import datetime
import logging
from typing import List

import pyqtgraph as pg
from PyQt6 import QtCore, QtGui, QtWidgets

from src.data import BASE_CURRENCIES, CRYPTO_CURRENCIES
from src.parser import parse_dataset


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.log = lambda *args_, **kwargs_: logging.log(logging.DEBUG + 5, *args_, **kwargs_)

        # Main window
        self.setWindowTitle("Crypto-predictor")
        self.setMinimumSize(600, 400)
        self.resize(900, 500)

        # Central widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Currencies group
        self.currencies_group = QtWidgets.QGroupBox()
        self.currencies_group.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.currencies_group.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum)

        # Currencies comboboxes
        self.fiat_curr = QtWidgets.QComboBox(self.currencies_group)
        self.crypto_curr = QtWidgets.QComboBox(self.currencies_group)
        self.fiat_curr.setMaxVisibleItems(30)
        self.crypto_curr.setMaxVisibleItems(30)

        # Slash-label between comboboxes
        slash_label = QtWidgets.QLabel("  /  ", self.currencies_group)
        slash_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        slash_label.setMinimumWidth(30)
        slash_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum)

        # Graph
        self.graph_item = pg.PlotItem()
        self.graph_item.setLabel("left", "Price")
        self.graph_item.setLabel("bottom", "Minutes")
        self.graph = pg.PlotWidget(self.central_widget, plotItem=self.graph_item)
        self.graph.setBackground(self.palette().color(QtGui.QPalette.ColorRole.Window))
        self.graph_item.addLegend()

        # Control panel
        self.control_group = QtWidgets.QGroupBox()
        self.control_group.setMaximumHeight(60)

        # Control run
        self.control_run = QtWidgets.QPushButton()
        self.control_run.setText("Run")
        self.control_run.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.control_run.setCheckable(True)
        self.control_run.clicked.connect(self._control_checkbox_run_event)

        # Control learn
        self.control_learn = QtWidgets.QPushButton()
        self.control_learn.setText("Learn")
        self.control_learn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.control_learn.setEnabled(False)
        self.control_learn.clicked.connect(self._control_learn_event)

        # Control predicate
        self.control_predicate = QtWidgets.QPushButton()
        self.control_predicate.setText("Predicate")
        self.control_predicate.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.control_predicate.setCheckable(True)
        self.control_predicate.setEnabled(False)
        self.control_predicate.clicked.connect(self._control_predicate_event)

        # Layouts
        self.central_widget_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.central_widget_layout.addWidget(self.currencies_group)
        self.central_widget_layout.addWidget(self.graph)
        self.central_widget_layout.addWidget(self.control_group)

        self.currencies_layout = QtWidgets.QHBoxLayout(self.currencies_group)
        self.currencies_layout.addWidget(self.crypto_curr)
        self.currencies_layout.addWidget(slash_label)
        self.currencies_layout.addWidget(self.fiat_curr)

        self.control_group_layout = QtWidgets.QHBoxLayout(self.control_group)
        self.control_group_layout.addWidget(self.control_run)
        self.control_group_layout.addWidget(self.control_learn)
        self.control_group_layout.addWidget(self.control_predicate)

        # Final logic
        self._fill_currencies_comboboxes()

    def _fill_currencies_comboboxes(self) -> None:
        for currency in BASE_CURRENCIES:
            self.fiat_curr.addItem(currency)
        self.fiat_curr.setCurrentText("USD")

        for currency in CRYPTO_CURRENCIES:
            self.crypto_curr.addItem(currency)
        self.crypto_curr.setCurrentText("BTC")

    def _control_checkbox_run_event(self, is_checked: bool) -> None:
        self.log(f"self._control_checkbox_run_event({is_checked=})")
        self.currencies_group.setEnabled(not is_checked)
        self.control_learn.setEnabled(is_checked)

        if not is_checked:
            self.graph_item.clear()
            return

        dataset, dataset_times = parse_dataset(f"{self.crypto_curr.currentText()}-{self.fiat_curr.currentText()}")
        item = pg.PlotDataItem(dataset_times, dataset, name="Actual price")
        self.graph_item.addItem(item)

    def _control_learn_event(self) -> None:
        self.control_learn.setEnabled(False)
        self.control_predicate.setEnabled(True)

    def _control_predicate_event(self, b):
        pass
