import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
import tkinter.ttk as ttk  # IMPORTANT: added proper import
import ipaddress
import time
from datetime import datetime

class PortScanner:
    def __init__(self, root):
        self.root = root
        self.is_scanning = False
        self.open_ports = []
        self.scan_thread = None
        self.start_time = None
        
        self.setup_gui()
        
    def setup_gui(self):
        self.root.title("Advanced Port Scanner")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Target IP
        tk.Label(main_frame, text="Target IP or Hostname:", font=("Arial", 10, "bold")).pack(pady=5)
        ip_frame = tk.Frame(main_frame)
        ip_frame.pack(fill=tk.X, pady=5)
        
        self.ip_entry = tk.Entry(ip_frame, width=50, font=("Arial", 10))
        self.ip_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.ip_entry.insert(0, "127.0.0.1")
        
        # Quick scan buttons
        quick_frame = tk.Frame(main_frame)
        quick_frame.pack(pady=5)
        
        tk.Button(quick_frame, text="Quick Scan (1-1024)", 
                  command=lambda: self.quick_scan(), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(quick_frame, text="Full Scan (1-65535)", 
                  command=lambda: self.full_scan(), bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(quick_frame, text="Common Ports", 
                  command=lambda: self.common_ports_scan(), bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Manual port range
        tk.Label(main_frame, text="Custom Port Range:", font=("Arial", 10, "bold")).pack(pady=5)
        port_frame = tk.Frame(main_frame)
        port_frame.pack(pady=5)
        
        tk.Label(port_frame, text="Start:").pack(side=tk.LEFT)
        self.start_port_entry = tk.Entry(port_frame, width=10, font=("Arial", 10))
        self.start_port_entry.pack(side=tk.LEFT, padx=5)
        self.start_port_entry.insert(0, "1")
        
        tk.Label(port_frame, text="End:").pack(side=tk.LEFT)
        self.end_port_entry = tk.Entry(port_frame, width=10, font=("Arial", 10))
        self.end_port_entry.pack(side=tk.LEFT, padx=5)
        self.end_port_entry.insert(0, "1024")
        
        # Scan options
        options_frame = tk.Frame(main_frame)
        options_frame.pack(pady=5)
        
        self.thread_var = tk.IntVar(value=50)
        tk.Label(options_frame, text="Threads:").pack(side=tk.LEFT)
        tk.Scale(options_frame, from_=1, to=200, orient=tk.HORIZONTAL, 
                 variable=self.thread_var, length=150).pack(side=tk.LEFT, padx=10)
        
        self.timeout_var = tk.DoubleVar(value=0.5)
        tk.Label(options_frame, text="Timeout (s):").pack(side=tk.LEFT)
        tk.Scale(options_frame, from_=0.1, to=5.0, orient=tk.HORIZONTAL, 
                 resolution=0.1, variable=self.timeout_var, length=150).pack(side=tk.LEFT, padx=10)
        
        # Scan button
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        self.scan_btn = tk.Button(button_frame, text="Start Custom Scan", 
                                 command=self.start_custom_scan,
                                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                                 padx=30, pady=5)
        self.scan_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="Stop Scan", 
                                 command=self.stop_scan,
                                 bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                                 padx=30, pady=5, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                              maximum=100, length=400)
        self.progress_bar.pack(pady=5)
        
        self.status_label = tk.Label(main_frame, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=5)
        
        # Results
        result_frame = tk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tk.Label(result_frame, text="Scan Results:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.result_box = scrolledtext.ScrolledText(result_frame, width=80, height=20, 
                                                   font=("Consolas", 9))
        self.result_box.pack(fill=tk.BOTH, expand=True)
        
        # Bind Enter key to start scan
        self.ip_entry.bind('<Return>', lambda e: self.start_custom_scan())
        
    def log(self, message):
        """Log message to result box"""
        self.result_box.insert(tk.END, message + "\n")
        self.result_box.see(tk.END)
        self.root.update()
        
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
        self.root.update()
        
    def stop_scan(self):
        """Stop the current scan"""
        self.is_scanning = False
        self.log("\n[!] Scan stopped by user")
        self.scan_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.update_status("Scan stopped")
        
    def is_valid_target(self, target):
        """Validate target IP or hostname"""
        try:
            # Try to resolve hostname
            socket.gethostbyname(target)
            return True
        except:
            return False
            
    def scan_port(self, target, port, timeout):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "Unknown"
                return (port, service)
        except:
            pass
        return None
        
    def scan_ports_range(self, target, start_port, end_port, num_threads, timeout):
        """Scan ports using threading"""
        self.is_scanning = True
        self.open_ports = []
        
        total_ports = end_port - start_port + 1
        ports_per_thread = max(1, total_ports // num_threads)
        threads = []
        results_lock = threading.Lock()
        scanned_count = [0]  # Use list for mutable reference in closure
        
        def scan_worker(thread_id):
            """Worker function for each thread"""
            my_start = start_port + (thread_id * ports_per_thread)
            if thread_id == num_threads - 1:
                my_end = end_port
            else:
                my_end = my_start + ports_per_thread - 1
            
            for port in range(my_start, my_end + 1):
                if not self.is_scanning:
                    break
                    
                result = self.scan_port(target, port, timeout)
                if result:
                    with results_lock:
                        self.open_ports.append(result)
                        self.log(f"[OPEN] Port {result[0]} ({result[1]})")
                
                # Update progress safely
                with results_lock:
                    scanned_count[0] += 1
                    progress = (scanned_count[0] / total_ports) * 100
                    self.progress_var.set(progress)
                    
                    if scanned_count[0] % 50 == 0 or scanned_count[0] == total_ports:
                        self.update_status(f"Scanning... {int(progress)}% complete ({scanned_count[0]}/{total_ports})")
        
        # Create and start threads
        for i in range(min(num_threads, total_ports)):
            thread = threading.Thread(target=scan_worker, args=(i,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            
        self.is_scanning = False
        
    def scan_ports(self, target, start_port, end_port):
        """Main scanning function"""
        if not self.is_valid_target(target):
            self.log(f"Error: Invalid target '{target}'")
            self.scan_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.update_status("Ready")
            return
            
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            self.log("Error: Invalid port range (1-65535)")
            self.scan_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.update_status("Ready")
            return
            
        num_threads = self.thread_var.get()
        timeout = self.timeout_var.get()
        
        self.start_time = datetime.now()
        self.log("=" * 60)
        self.log(f"Starting scan on {target}")
        self.log(f"Port range: {start_port} - {end_port}")
        self.log(f"Threads: {num_threads}, Timeout: {timeout}s")
        self.log("=" * 60)
        self.log("")
        
        self.update_status("Initializing...")
        self.progress_var.set(0)
        
        try:
            # Perform scan
            self.scan_ports_range(target, start_port, end_port, num_threads, timeout)
            
            # Show results
            elapsed = datetime.now() - self.start_time
            self.log("")
            self.log("=" * 60)
            self.log(f"Scan completed in {elapsed.total_seconds():.2f} seconds")
            
            if self.is_scanning:  # Only if not stopped by user
                self.log(f"Open ports found: {len(self.open_ports)}")
                
                if self.open_ports:
                    self.log("Open ports:")
                    for port, service in sorted(self.open_ports):
                        self.log(f"  {port}: {service}")
                else:
                    self.log("No open ports found")
                self.log("=" * 60)
            
        except Exception as e:
            self.log(f"Error during scan: {str(e)}")
            
        finally:
            # Re-enable scan button
            self.scan_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.update_status("Ready")
            
    # Quick scan functions
    def quick_scan(self):
        target = self.ip_entry.get().strip()
        self.scan_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        scan_thread = threading.Thread(target=self.scan_ports, args=(target, 1, 1024))
        scan_thread.daemon = True
        scan_thread.start()
        
    def full_scan(self):
        target = self.ip_entry.get().strip()
        self.scan_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        scan_thread = threading.Thread(target=self.scan_ports, args=(target, 1, 65535))
        scan_thread.daemon = True
        scan_thread.start()
        
    def common_ports_scan(self):
        """Scan only common ports"""
        target = self.ip_entry.get().strip()
        
        if not self.is_valid_target(target):
            self.log(f"Error: Invalid target '{target}'")
            return
        
        self.scan_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Run in thread to avoid blocking GUI
        scan_thread = threading.Thread(target=self._common_ports_worker, args=(target,))
        scan_thread.daemon = True
        scan_thread.start()
        
    def _common_ports_worker(self, target):
        """Worker for common ports scan"""
        common_ports = [20, 21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 
                       1723, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017]
        
        self.is_scanning = True
        self.open_ports = []
        self.log("=" * 60)
        self.log(f"Scanning common ports on {target}")
        self.log("=" * 60)
        
        for i, port in enumerate(common_ports):
            if not self.is_scanning:
                break
                
            result = self.scan_port(target, port, self.timeout_var.get())
            if result:
                self.open_ports.append(result)
                self.log(f"[OPEN] Port {result[0]} ({result[1]})")
            
            progress = ((i + 1) / len(common_ports)) * 100
            self.progress_var.set(progress)
            self.update_status(f"Scanning common ports... {int(progress)}%")
        
        self.log("")
        self.log(f"Common ports scan complete. Found {len(self.open_ports)} open ports.")
        self.is_scanning = False
        self.scan_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.update_status("Ready")
        
    def start_custom_scan(self):
        """Start custom port range scan"""
        if self.is_scanning:
            messagebox.showwarning("Warning", "A scan is already in progress. Stop it first.")
            return
            
        target = self.ip_entry.get().strip()
        
        if not target:
            messagebox.showerror("Error", "Please enter a target IP or hostname.")
            return
            
        try:
            start_port = int(self.start_port_entry.get())
            end_port = int(self.end_port_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid port numbers.")
            return
            
        # Disable scan button and enable stop button
        self.scan_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Run scan in separate thread
        scan_thread = threading.Thread(target=self.scan_ports, args=(target, start_port, end_port))
        scan_thread.daemon = True
        scan_thread.start()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = PortScanner(root)
    root.mainloop()