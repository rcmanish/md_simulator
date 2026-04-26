#!/usr/bin/env python3
"""
generate_profiling_latex_table.py
Reads data/profiling_table.csv and emits a complete LaTeX table.
Also prints the table for copy-paste into the paper.
"""
import pandas as pd, sys

df = pd.read_csv("data/profiling_table.csv")

print(r"""\begin{table}[htbp]
\caption{Serial Profiling Results: Wall Time by Function}
\label{tab:profiling}
\begin{center}
\begin{tabular}{|l|c|c|c|c|c|}
\hline
\textbf{Function} & \textbf{N=100} & \textbf{N=200} & \textbf{N=500} & \textbf{N=1000} & \textbf{N=2000} \\
& \textbf{T(s)} & \textbf{T(s)} & \textbf{T(s)} & \textbf{T(s)} & \textbf{T(s)} \\
\hline""")

fields = ["forces_s","verlet_s","pbc_s","io_s","total_s"]
labels = ["compute\_forces","velocity\_verlet","apply\_pbc","I/O \& Thermo","TOTAL"]
data = {row["N"]: row for _, row in df.iterrows()}
Ns = sorted(data.keys())

for field, label in zip(fields, labels):
    row = label
    for N in Ns:
        if N not in [100, 200, 500, 1000, 2000]: continue
        row += f" & {data[N][field]:.4f}"
    row += r" \\"
    print(row)
    if label == "I/O \& Thermo":
        print(r"\hline")

print(r"""\hline
\end{tabular}
\end{center}
\vspace{2pt}
{\footnotesize All runs: 500 steps, $\rho=0.8$, $r_c=2.5$, serial.}
\end{table}""")

# Runtime table
print("\n\n% === Runtime Table ===")
rt = pd.read_csv("data/runtime_table.csv")

print(r"""\begin{table*}[htbp]
\caption{MD Runtime, Speedup, and Efficiency Summary (N=2000, 500 steps)}
\label{tab:runtime}
\begin{center}
\begin{tabular}{|l|c|c|c|c|c|}
\hline
\textbf{Mode} & \textbf{Threads/Ranks} & \textbf{$T_p$ (s)} & \textbf{$S(p)$} & \textbf{$E(p)$} & \textbf{Data Source} \\
\hline""")
for _, row in rt.iterrows():
    print(f"{row['mode']} & {row['threads_or_ranks']} & {float(row['T_wall_s']):.3f} & "
          f"{float(row['speedup']):.3f} & {float(row['efficiency']):.3f} & "
          f"{row['data_source'].replace('_',' ')} \\\\")
print(r"""\hline
\end{tabular}
\end{center}
\end{table*}""")
