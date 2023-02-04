#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import gspread
from google.oauth2 import service_account

# https://docs.gspread.org/en/latest/user-guide.html


# ==========================
# Global Variables
# ==========================
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class Record:
    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol
        self.five_yr_pps = 0  # five year price per share average
        self.net_income = 0
        self.pref_div = 0  # preferred dividends
        self.outstanding = 0  # oustanding shares
        self.pps = 0.00  # price per share

        # formula to compute
        self.basic_eps = 0.00
        self.formula_basic_eps = ""
        self.pe_ratio = 0.00
        self.formula_pe_ration = ""
        self.cagar = 0.00
        self.formula_cagr = ""
        self.ben_graham = 0.00
        self.formula_ben_graham = ""
        self.graham_ratio = 0.00
        self.formula_graham_ratio = ""
        self.notes = ""

    def calc_basic_eps(self, row):
        # calculates basic earnings per share and cell formula for google sheet
        self.basic_eps = (self.net_income - self.pref_div) / self.outstanding
        formula = "=(Cr-Dr)/Er"
        self.formula_basic_eps = formula.replace("r", str(row))

    def calc_pe_ratio(self, row):
        # calculates price-to-earnings ratio rand cell formula for google sheet
        if self.basic_eps == 0.00:
            self.calc_basic_eps(row)
        self.pe_ratio = self.pps / self.basic_eps
        formula = "=Fr/Gr"
        self.formula_pe_ratio = formula.replace("r", str(row))

    def calc_cagr(self, row):
        self.cagr = pow((self.pps / self.five_yr_pps), (1 / 5)) - 1
        formula = "=((Fr/Br)^(1/5))-1"
        self.formula_cagr = formula.replace("r", str(row))

    def calc_ben_graham(self, row):
        if self.basic_eps == 0.00:
            self.calc_basic_eps(row)
        if self.pe_ratio == 0.00:
            self.calc_pe_ratio(row)
        if self.cagr == 0.00:
            self.calc_cagr(row)
        self.ben_graham = self.basic_eps * (self.pe_ratio + self.cagr)
        formula = "=Gr*(Hr+Ir)"
        self.formula_ben_graham = formula.replace("r", str(row))

    def calc_graham_ratio(self, row):
        if self.ben_graham == 0.00:
            self.calc_ben_graham(row)
        self.graham_ratio = (self.ben_graham / self.pps) - 1
        formula = "=(Jr/Fr)-1"
        self.formula_graham_ratio = formula.replace("r", str(row))

    def calc_all(self, row):
        self.calc_basic_eps(row)
        self.calc_pe_ratio(row)
        self.calc_cagr(row)
        self.calc_ben_graham(row)
        self.calc_graham_ratio(row)


# ==========================
# Functions
# ==========================


def err(msg=None):
    """
    Converts string to bytes & Outputs to stderr
    """
    if not msg:
        return
    msg = msg + "\n"
    os.write(2, msg.encode())


def auth(cred_filename="service.json", scopes=SCOPES):
    # authenticates and authorize to google drive/sheets
    credentials = service_account.Credentials.from_service_account_file(
        cred_filename, scopes=scopes
    )
    gc = gspread.authorize(credentials)
    return gc


def format(worksheet):
    pass


def append(worksheet, rec):
    # get last row, update calculations then write
    row = len(worksheet.col_values(1)) + 1
    rec.calc_all(row)
    worksheet.update_cell(row, 1, rec.stock_symbol)
    worksheet.update_cell(row, 2, rec.five_yr_pps)
    worksheet.update_cell(row, 3, rec.net_income)
    worksheet.update_cell(row, 4, rec.pref_div)
    worksheet.update_cell(row, 5, rec.outstanding)
    worksheet.update_cell(row, 6, rec.pps)
    worksheet.update_cell(row, 7, rec.formula_basic_eps)
    worksheet.update_cell(row, 8, rec.formula_pe_ratio)
    worksheet.update_cell(row, 9, rec.formula_cagr)
    worksheet.update_cell(row, 10, rec.formula_ben_graham)
    worksheet.update_cell(row, 11, rec.formula_graham_ratio)


# ----------------------------------------------------------------------
# M A I N  L O G I C
# ----------------------------------------------------------------------


def main():
    gc = auth()

    # get Google Sheet and worksheet
    sh = gc.open("Stock Market Analysis - Valuation")
    ws = sh.worksheet("valuations")

    print(ws.acell("B1").value)

    # cell formula
    print(ws.acell("F2", value_render_option="FORMULA").value)

    # all values from first row
    print(ws.row_values(1))

    # all values from first column
    print(ws.col_values(1))

    # get last row then write
    rec = Record("Test")
    rec.five_yr_pps = 325.50
    rec.net_income = 5044069
    rec.pref_div = 0
    rec.outstanding = 443155
    rec.pps = 360.04
    append(ws, rec)


if __name__ == "__main__":
    main()
    sys.exit(0)
