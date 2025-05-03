#!/usr/bin/env python
"""
Test script to run pyptv_batch on the test_cavity directory.
"""
import sys
import os
import shutil
from pathlib import Path

# Import the openptv module
import openptv
from openptv.gui.pyptv_batch import main

def run_test(test_cavity_path):
    """Run the batch processing on the test_cavity directory."""
    test_dir = Path(test_cavity_path)
    if not test_dir.exists():
        print(f"Test directory {test_dir} not found")
        return False

    # Define frame range
    start_frame = 10000
    end_frame = 10004

    # Save current directory
    original_dir = os.getcwd()

    # Path to the res directory
    res_dir = test_dir / "res"

    # Backup existing res directory if it exists
    backup_dir = None
    if res_dir.exists():
        backup_dir = test_dir / "res_backup"
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(res_dir, backup_dir)
        shutil.rmtree(res_dir)

    # Create a fresh res directory
    res_dir.mkdir(exist_ok=True)

    try:
        # Update the path in the ptv.yaml file
        ptv_yaml_path = test_dir / "parameters" / "ptv.yaml"
        if ptv_yaml_path.exists():
            import yaml
            with open(ptv_yaml_path, 'r') as f:
                ptv_config = yaml.safe_load(f)

            # Update the path to the current directory
            ptv_config['path'] = str(test_dir / "parameters")

            with open(ptv_yaml_path, 'w') as f:
                yaml.dump(ptv_config, f)

            print(f"Updated path in {ptv_yaml_path} to {ptv_config['path']}")

        # Run the batch processing
        print(f"\nRunning batch processing on {test_dir} for frames {start_frame}-{end_frame}")
        os.chdir(test_dir)
        # Use the absolute path to avoid path issues
        main(os.path.abspath('.'), start_frame, end_frame)

        # List all files in the res directory
        print("\nFiles in res directory:")
        for file in sorted(res_dir.glob("*")):
            print(f"  {file.name}")

        # Check for tracking files
        tracking_files = list(res_dir.glob("ptv_is.*"))
        if tracking_files:
            print(f"\nTracking completed successfully! Found {len(tracking_files)} tracking files.")

            # Check for correspondence files
            corresp_files = list(res_dir.glob("rt_is.*"))
            if corresp_files:
                print(f"Correspondence completed successfully! Found {len(corresp_files)} correspondence files.")
            else:
                print("No correspondence files found.")

            # Check for added particles files
            added_files = list(res_dir.glob("added.*"))
            if added_files:
                print(f"Added particles files found: {len(added_files)} files.")
            else:
                print("No added particles files found.")

            # Verify we have the expected number of files
            if len(tracking_files) == (end_frame - start_frame + 1):
                print(f"✅ Found expected number of tracking files: {len(tracking_files)}")
            else:
                print(f"❌ Expected {end_frame - start_frame + 1} tracking files, found {len(tracking_files)}")

            if len(corresp_files) == (end_frame - start_frame + 1):
                print(f"✅ Found expected number of correspondence files: {len(corresp_files)}")
            else:
                print(f"❌ Expected {end_frame - start_frame + 1} correspondence files, found {len(corresp_files)}")

            if len(added_files) == (end_frame - start_frame + 1):
                print(f"✅ Found expected number of added particles files: {len(added_files)}")
            else:
                print(f"❌ Expected {end_frame - start_frame + 1} added particles files, found {len(added_files)}")
        else:
            print("\nNo tracking files found. Tracking may not have completed.")
            return False

        print("\nFull sequence and tracking test completed successfully!")
        return True

    except Exception as e:
        print(f"Batch processing or verification failed: {str(e)}")
        return False
    finally:
        # Change back to the original directory
        os.chdir(original_dir)

        # Clean up: remove the res directory created during the test
        if res_dir.exists():
            shutil.rmtree(res_dir)

        # Restore the original res directory if it existed
        if backup_dir is not None and backup_dir.exists():
            shutil.copytree(backup_dir, res_dir)
            shutil.rmtree(backup_dir)

if __name__ == "__main__":
    """Run the test directly."""
    if len(sys.argv) < 2:
        print("Usage: python run_test.py <path_to_test_cavity>")
        sys.exit(1)

    test_cavity_path = sys.argv[1]
    print(f"Running test on {test_cavity_path}")

    success = run_test(test_cavity_path)
    if success:
        print("\n✅ Full PyPTV batch sequence test passed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Full PyPTV batch sequence test failed!")
        sys.exit(1)
