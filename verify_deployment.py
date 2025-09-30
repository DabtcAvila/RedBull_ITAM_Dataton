#!/usr/bin/env python3
"""
CasaMX Deployment Verification Script
Datatón ITAM 2025

Este script verifica que el deployment esté funcionando correctamente
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple
import sys

class DeploymentVerifier:
    def __init__(self, base_url: str = "https://casamx.store"):
        self.base_url = base_url.rstrip('/')
        self.results = []
        
    def log_result(self, test_name: str, success: bool, details: str = "", response_time: float = 0):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        if response_time > 0:
            print(f"    Response time: {response_time:.2f}s")
        print()
        
    def test_main_site(self) -> bool:
        """Test main Streamlit site"""
        try:
            start_time = time.time()
            response = requests.get(self.base_url, timeout=10)
            response_time = time.time() - start_time
            
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                # Check for Streamlit indicators
                if "streamlit" in response.text.lower() or "casamx" in response.text.lower():
                    details += " | Streamlit app detected"
                else:
                    success = False
                    details += " | Streamlit content not detected"
                    
            self.log_result("Main Site (Streamlit)", success, details, response_time)
            return success
            
        except Exception as e:
            self.log_result("Main Site (Streamlit)", False, f"Error: {str(e)}")
            return False
            
    def test_api_endpoint(self) -> bool:
        """Test FastAPI endpoint"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/api/", timeout=10)
            response_time = time.time() - start_time
            
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                try:
                    data = response.json()
                    if "message" in data:
                        details += f" | Message: {data.get('message', 'N/A')}"
                    else:
                        details += " | Valid JSON response"
                except:
                    details += " | Non-JSON response"
                    
            self.log_result("API Endpoint (FastAPI)", success, details, response_time)
            return success
            
        except Exception as e:
            self.log_result("API Endpoint (FastAPI)", False, f"Error: {str(e)}")
            return False
            
    def test_api_docs(self) -> bool:
        """Test API documentation"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/api/docs", timeout=10)
            response_time = time.time() - start_time
            
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success and "swagger" in response.text.lower():
                details += " | Swagger UI available"
            elif success:
                details += " | Docs accessible"
                
            self.log_result("API Documentation", success, details, response_time)
            return success
            
        except Exception as e:
            self.log_result("API Documentation", False, f"Error: {str(e)}")
            return False
            
    def test_ssl_certificate(self) -> bool:
        """Test SSL certificate"""
        try:
            start_time = time.time()
            response = requests.get(self.base_url, timeout=10, verify=True)
            response_time = time.time() - start_time
            
            success = response.url.startswith('https://')
            details = f"HTTPS redirect: {'Yes' if success else 'No'}"
            
            self.log_result("SSL Certificate", success, details, response_time)
            return success
            
        except Exception as e:
            self.log_result("SSL Certificate", False, f"Error: {str(e)}")
            return False
            
    def test_performance(self) -> bool:
        """Test performance metrics"""
        try:
            times = []
            for i in range(3):
                start_time = time.time()
                response = requests.get(self.base_url, timeout=15)
                response_time = time.time() - start_time
                times.append(response_time)
                time.sleep(1)
                
            avg_time = sum(times) / len(times)
            success = avg_time < 5.0  # Less than 5 seconds average
            details = f"Average response time: {avg_time:.2f}s (3 requests)"
            
            if success:
                details += " | Performance OK"
            else:
                details += " | Performance slow (>5s)"
                
            self.log_result("Performance Test", success, details, avg_time)
            return success
            
        except Exception as e:
            self.log_result("Performance Test", False, f"Error: {str(e)}")
            return False
            
    def run_all_tests(self) -> Tuple[bool, Dict]:
        """Run all verification tests"""
        print("🚀 Starting CasaMX Deployment Verification")
        print("="*50)
        print()
        
        tests = [
            ("Main Site", self.test_main_site),
            ("API Endpoint", self.test_api_endpoint),
            ("API Docs", self.test_api_docs),
            ("SSL Certificate", self.test_ssl_certificate),
            ("Performance", self.test_performance)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            if test_func():
                passed += 1
                
        print("="*50)
        print(f"SUMMARY: {passed}/{total} tests passed")
        
        overall_success = passed == total
        if overall_success:
            print("🎉 ALL TESTS PASSED - CasaMX is ready for Datatón ITAM 2025!")
        else:
            print("⚠️  Some tests failed - please check the issues above")
            
        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "tests_passed": passed,
            "tests_total": total,
            "success_rate": (passed / total) * 100,
            "overall_success": overall_success,
            "results": self.results
        }
        
        return overall_success, report
        
    def save_report(self, report: Dict, filename: str = "deployment_report.json"):
        """Save verification report to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"📋 Report saved to: {filename}")
        except Exception as e:
            print(f"❌ Failed to save report: {e}")

def main():
    """Main function"""
    # Allow custom URL via command line
    url = sys.argv[1] if len(sys.argv) > 1 else "https://casamx.store"
    
    verifier = DeploymentVerifier(url)
    success, report = verifier.run_all_tests()
    
    # Save report
    verifier.save_report(report)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()