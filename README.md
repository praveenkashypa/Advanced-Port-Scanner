# Advanced-Port-Scanner

# Overview

The Advanced Port Scanner is a Python-based cybersecurity application designed to identify open TCP ports and running network services on a target host. It provides a user-friendly graphical interface (GUI) built with Tkinter and supports quick scans, full scans, common port scans, and custom port range scanning using multithreading for high-speed performance.

# Features

# 1. Quick Port Scan

Scans ports 1–1024, covering the most commonly used network services.

Purpose
Fast reconnaissance
Identify common services
Initial security assessment
2. Full Port Scan

Scans the complete TCP port range from 1–65535.

Purpose
Discover all open ports
Identify hidden services
Complete network assessment


# 3. Common Ports Scan

Scans only frequently used ports.

Examples
FTP (21)
SSH (22)
HTTP (80)
HTTPS (443)
MySQL (3306)
RDP (3389)
Redis (6379)
HTTP Proxy (8080)
Benefits
Faster scanning
Focuses on widely used services
Ideal for quick reconnaissance

# 4. Custom Port Range Scan

Allows users to specify a custom range of ports for scanning.

Benefits
Flexible scanning
Saves time by targeting specific ports
Useful during penetration testing

# 5. TCP Port Detection

Identifies open TCP ports on the target system.

Displays
Port Number
Port Status
Running Service

# 6. Service Detection

Automatically identifies the default service running on open ports.

Example
22 → SSH
80 → HTTP
443 → HTTPS
3306 → MySQL

# 7. Multi-threaded Scanning

Uses multiple threads to scan ports simultaneously.

Benefits
Faster scanning
Better performance
Efficient resource utilization

# 8. Scan Progress Monitoring

Displays the scanning progress in real time.

Information Displayed
Percentage Completed
Ports Scanned
Current Status
Scan Progress Bar

# 9. Scan Control

Provides complete control over the scanning process.

Features
Start Scan
Stop Scan
Real-time Status Updates

# 10. Graphical User Interface (GUI)

# Built using Tkinter to provide an easy-to-use interface.

Interface Includes
Target Input
Quick Scan Button
Full Scan Button
Common Ports Scan
Custom Port Range
Thread Configuration
Timeout Configuration
Progress Bar
Scan Results Window

# 11. Scan Results

# Displays detailed scan information including:

Open Ports
Service Names
Scan Duration
Total Open Ports
Scan Summary
Technologies Used
Python 3
Tkinter
Socket Programming
Multithreading
TCP/IP Networking
Thread Synchronization
Applications

# This project can be used for:

Network Reconnaissance
Port Discovery
Security Auditing
Vulnerability Assessment
Penetration Testing
Network Administration
Cybersecurity Training
Infrastructure Assessment
Skills Demonstrated

# This project demonstrates knowledge of:

Python Programming
Socket Programming
TCP/IP Networking
Multithreading
GUI Development
Network Security
Port Scanning Techniques
Cybersecurity Fundamentals
Performance Optimization

# Disclaimer
This project is intended solely for educational purposes and authorized security testing. Users must obtain explicit permission before scanning or testing any systems or networks. Unauthorized use may violate applicable laws and regulations.

GitHub Short Description (≤350 characters)
