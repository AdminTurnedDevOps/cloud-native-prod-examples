#!/usr/bin/env python3
"""
Performance comparison test between pip and uv for Django development.
Tests virtual environment creation, package installation, and Django startup times.
"""

import subprocess
import time
import os
import shutil

print("Starting Django pip vs uv Performance Comparison")
time.sleep(2)

def create_test_dirs():
    if not os.path.exists('test_pip'):
        os.makedirs('test_pip')
    if not os.path.exists('test_uv'):
        os.makedirs('test_uv')


def time_command(command, description, cwd=None):
    print(f"\nTesting: {description}")
    print(f"Command: {command}")
    
    start_time = time.time()
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=cwd,
            timeout=300  # 5 minute timeout
        )
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"Success: {duration:.2f} seconds")
            return duration
        else:
            print(f"Failed: {result.stderr}")
            return None
        
    except subprocess.TimeoutExpired:
        print(f"Timeout after 5 minutes")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_venv_creation():
    print("\n" + "="*60)
    print("VIRTUAL ENVIRONMENT CREATION TEST")
    print("="*60)
        
    pip_time = time_command(
        "cd test_pip && python3 -m venv venv && cd ..",
        "pip: Virtual environment creation"
    )
     
    uv_time = time_command(
        "cd test_uv && uv venv && cd ..",
        "uv: Virtual environment creation"
    )
    
    return pip_time, uv_time


def test_package_installation():
    print("\n" + "="*60)
    print("PACKAGE INSTALLATION TEST")
    print("="*60)
    
    pip_time = time_command(
        "source venv/bin/activate && pip install django",
        "pip: Django installation",
        cwd="test_pip"
    )
    
    uv_time = time_command(
        "uv pip install django",
        "uv: Django installation", 
        cwd="test_uv"
    )
    
    return pip_time, uv_time


def test_django_project_creation():
    print("\n" + "="*60)
    print("DJANGO PROJECT CREATION TEST")
    print("="*60)
    
    pip_time = time_command(
        "source venv/bin/activate && django-admin startproject testproject . && cd ..",
        "pip: Django project creation",
        cwd="test_pip"
    )
    
    uv_time = time_command(
        "uv run django-admin startproject testproject . && cd ..",
        "uv: Django project creation",
        cwd="test_uv"
    )
    
    return pip_time, uv_time


def test_django_startup():
    print("\n" + "="*60)
    print("DJANGO SERVER STARTUP TEST")
    print("="*60)
    
    pip_time = time_command(
        "source venv/bin/activate && python manage.py check",
        "pip: Django system check",
        cwd="test_pip"
    )
    
    uv_time = time_command(
        "uv run python manage.py check",
        "uv: Django system check",
        cwd="test_uv"
    )
    
    return pip_time, uv_time


def print_summary(results):
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON SUMMARY")
    print("="*60)
    
    for name, (pip_time, uv_time) in results.items():
        if pip_time and uv_time:
            print(f"\n{name}:")
            print(f"  pip:  {pip_time:.2f}s")
            print(f"  uv:   {uv_time:.2f}s")
        else:
            print(f"\n{name}: Unable to complete comparison")


def cleanup_test_dirs():
    test_dirs = ['test_pip', 'test_uv']
    for dir_name in test_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)


def main():
    create_test_dirs()
    
    print("Below Are the Results of the Performance Comparison Tests:")
    
    results = {}
    
    results['Virtual Environment Creation Test'] = test_venv_creation()
    results['Package Installation Test'] = test_package_installation()
    results['Django Project Creation Test'] = test_django_project_creation()
    results['Django System Check Test'] = test_django_startup()

    print_summary(results)
    
    print("\nCleaning up test directories...")
    cleanup_test_dirs()
    for dir_name in ['fresh_pip', 'fresh_uv']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    time.sleep(2)
    print("\nPerformance comparison complete!")


if __name__ == "__main__":
    main()