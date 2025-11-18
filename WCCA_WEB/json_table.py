# json_table.py
from tkinter import ttk


def show_json_table(
    container,
    data,
    tree_style="",
    heading_style="",
    vscroll_style="",
    hscroll_style="",
    columns=None,
    max_rows=500,
    height_rows=12,
):
    # Clear previous widgets
    for child in container.winfo_children():
        child.destroy()

    # Columns: preferred first, then any others found in data
    preferred = ["Part Number", "Mfr", "Part Status"]
    cols = columns[:] if columns else []
    if not cols:
        cols = [c for c in preferred if any(c in row for row in data)]
        seen = set(cols)
        for row in data:
            for k in row.keys():
                if k not in seen:
                    cols.append(k)
                    seen.add(k)

    tree = ttk.Treeview(container, columns=cols, show="headings", style=tree_style, height=height_rows)

    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=160, anchor="w")

    # Rows
    for row in data[:max_rows]:
        values = [row.get(c, "") for c in cols]
        tree.insert("", "end", values=values)

    # Scrollbars
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview, style=vscroll_style)
    hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview, style=hscroll_style)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Layout
    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    # Optional: enable basic column-resize on double-click header
    def autosize_col(col_id):
        maxw = max([len(str(tree.set(iid, col_id))) for iid in tree.get_children("")] + [len(col_id)])
        tree.column(col_id, width=min(maxw * 8 + 24, 360))

    def on_heading_click(col_id):
        autosize_col(col_id)

    for c in cols:
        tree.heading(c, text=c, command=lambda cid=c: on_heading_click(cid))

    return tree


def show_categorized_tables(
    container,
    data,
    tree_style="",
    heading_style="",
    vscroll_style="",
    hscroll_style="",
    height_rows=12,
):
    # Clear container
    for child in container.winfo_children():
        child.destroy()

    # Split into CAP and RES
    caps = [d for d in data if "Capacitance" in d]
    ress = [d for d in data if "Resistance" in d]

    # Table specs
    cap_cols = [
        "Part Number",
        "Mfr",
        "Capacitance",
        "Tolerance",
        "Temperature Coefficient",
        "Operating Temperature",
    ]
    res_cols = [
        "Part Number",
        "Mfr",
        "Resistance",
        "Tolerance",
        "Temperature Coefficient",
        "Operating Temperature",
    ]

    # Use a tabbed notebook to reduce whitespace and switch between categories
    nb = ttk.Notebook(container)
    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)
    nb.grid(row=0, column=0, sticky="nsew")

    added = False
    if caps:
        cap_frame = ttk.Frame(nb)
        nb.add(cap_frame, text="CAP")
        show_json_table(
            cap_frame, caps,
            tree_style=tree_style,
            heading_style=heading_style,
            vscroll_style=vscroll_style,
            hscroll_style=hscroll_style,
            columns=cap_cols,
            height_rows=height_rows,
        )
        added = True

    if ress:
        res_frame = ttk.Frame(nb)
        nb.add(res_frame, text="RES")
        show_json_table(
            res_frame, ress,
            tree_style=tree_style,
            heading_style=heading_style,
            vscroll_style=vscroll_style,
            hscroll_style=hscroll_style,
            columns=res_cols,
            height_rows=height_rows,
        )
        added = True

    if not added:
        # nothing matched; show an empty state
        msg = ttk.Label(container, text="No Capacitors or Resistors found in JSON.")
        msg.grid(row=0, column=0, sticky="w", padx=4, pady=4)