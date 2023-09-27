import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *

app = ttk.Window()
colors = app.style.colors

coldata = [
    {"text": "LicenseNumber", "stretch": False, },
    "CompanyName",
    {"text": "UserCount", "stretch": False},
]

rowdata = [
    ('A123', 'IzzyCo', 12),
    ('A136', 'Kimdee Inc.', 45),
    ('A158', 'Farmadding Co.', 36)
]

dt = Tableview(
    master=app,
    bootstyle=PRIMARY,
    coldata=coldata,
    rowdata=rowdata,
    paginated=True,
    searchable=True,
    autofit=False,
    autoalign=True,
    stripecolor=(colors.light, None),
    pagesize=10,
    height=10,
    delimiter=','
)
dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)

app.mainloop()
