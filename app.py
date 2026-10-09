import tkinter as tk
from tkinter import messagebox
import socket
import ipaddress

# Ports selected for this educational checker
PORTS = [80, 443, 445, 3389, 8000, 8080]


def scan_ports():
    target = ip_entry.get().strip()

    # Validate the IP address
    try:
        ip = ipaddress.ip_address(target)

        if ip.version != 4:
            raise ValueError("IPv4 addresses only.")

        if not (ip.is_private or ip.is_loopback):
            messagebox.showerror(
                "Not allowed",
                "Use localhost or an authorized private IPv4 address."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Invalid IP",
            "Enter a valid IPv4 address, e.g. 127.0.0.1"
        )
        return

    scan_button.config(state="disabled")
    results.delete("1.0", tk.END)
    results.insert(tk.END, f"Target: {target}\n")
    results.insert(tk.END, "-" * 35 + "\n")
    window.update_idletasks()

    try:
        for port in PORTS:
            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )
            sock.settimeout(0.4)

            try:
                status = sock.connect_ex((target, port))

                if status == 0:
                    result = "OPEN"
                else:
                    result = "NOT OPEN / NO RESPONSE"

                results.insert(
                    tk.END,
                    f"Port {port}: {result}\n"
                )

            except OSError:
                results.insert(
                    tk.END,
                    f"Port {port}: CONNECTION ERROR\n"
                )

            finally:
                sock.close()

    finally:
        results.insert(tk.END, "\nScan finished.\n")
        scan_button.config(state="normal")


# Create the main window
window = tk.Tk()
window.title("CyberCheck")
window.geometry("520x430")
window.configure(bg="#20242c")
window.resizable(False, False)

# Heading
heading = tk.Label(
    window,
    text="CyberCheck - Port Checker",
    font=("Arial", 17, "bold"),
    fg="white",
    bg="#20242c"
)
heading.pack(pady=(20, 10))

# Target IP
ip_label = tk.Label(
    window,
    text="Target IPv4 address:",
    font=("Arial", 11),
    fg="white",
    bg="#20242c"
)
ip_label.pack()

ip_entry = tk.Entry(
    window,
    font=("Arial", 12),
    justify="center",
    width=25
)
ip_entry.insert(0, "127.0.0.1")
ip_entry.pack(pady=8)

# Scan button
scan_button = tk.Button(
    window,
    text="Scan Ports",
    font=("Arial", 11, "bold"),
    bg="#4caf50",
    fg="white",
    activebackground="#388e3c",
    command=scan_ports
)
scan_button.pack(pady=8)

# Results area
results = tk.Text(
    window,
    height=12,
    width=55,
    font=("Consolas", 10),
    bg="#15181e",
    fg="#b8f7c5",
    insertbackground="white"
)
results.pack(padx=15, pady=10)

# Start the application
window.mainloop()