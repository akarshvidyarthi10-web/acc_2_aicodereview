"""
Comprehensive test to verify all components:
- Health endpoint
- MongoDB connection
- Gemini integration
- GitHub webhook secret verification
"""
import asyncio
import json
import hmac
import hashlib
from config.settings import settings
from services.ai_service import analyze_code
from services.db_service import save_review, list_reviews
from services.github_service import get_pr_files
from utils.github_webhook import verify_github_signature


async def test_health_endpoint():
    """Test if health endpoint is accessible"""
    print("\n🏥 Testing Health Endpoint...")
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✅ Health endpoint: OK")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return False


async def test_root_endpoint():
    """Test if root endpoint is accessible"""
    print("\n📡 Testing Root Endpoint...")
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/")
            if response.status_code == 200:
                print("✅ Root endpoint: OK")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ Root endpoint failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Error testing root endpoint: {e}")
        return False


async def test_mongodb_connection():
    """Test MongoDB connection and save/retrieve"""
    print("\n🗄️  Testing MongoDB Connection...")
    try:
        # Test write
        test_review = {
            "repo_full_name": "test/repo",
            "pr_number": 1,
            "summary": "Test review",
            "security": [],
            "smells": [],
            "review_score": 85,
        }
        result = await save_review(test_review)
        if result:
            print("✅ MongoDB write: OK")
            print(f"   Saved review ID: {result.get('id')}")
            
            # Test read
            reviews = await list_reviews()
            if reviews:
                print("✅ MongoDB read: OK")
                print(f"   Retrieved {len(reviews)} reviews")
                return True
            else:
                print("❌ MongoDB read failed")
                return False
        else:
            print("❌ MongoDB write failed")
            return False
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_gemini_integration():
    """Test Gemini API integration"""
    print("\n🤖 Testing Gemini Integration...")
    try:
        if not settings.gemini_api_key:
            print("❌ GEMINI_API_KEY not set in environment")
            return False
        
        if not settings.gemini_model:
            print("❌ GEMINI_MODEL not set in environment")
            return False
        
        # Test with a simple diff
        test_diff = """
--- a/app.py
+++ b/app.py
@@ -1,3 +1,4 @@
+password = "secret123"
 def login():
     pass
"""
        
        result = await analyze_code(test_diff)
        
        if result and "summary" in result:
            print("✅ Gemini integration: OK")
            print(f"   Model: {result.get('model')}")
            print(f"   Summary: {result.get('summary')[:100]}...")
            print(f"   Security issues: {len(result.get('security', []))}")
            print(f"   Code smells: {len(result.get('smells', []))}")
            print(f"   Review score: {result.get('review_score')}/100")
            return True
        else:
            print("❌ Gemini response invalid")
            return False
    except Exception as e:
        print(f"❌ Gemini integration error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_webhook_signature_verification():
    """Test GitHub webhook signature verification"""
    print("\n🔐 Testing Webhook Signature Verification...")
    try:
        if not settings.github_webhook_secret:
            print("❌ GITHUB_WEBHOOK_SECRET not set in environment")
            return False
        
        # Create a test payload
        payload = json.dumps({"test": "payload"}).encode()
        
        # Generate signature with secret
        signature = "sha256=" + hmac.new(
            settings.github_webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        # Verify the signature - this function raises HTTPException on failure
        try:
            verify_github_signature(signature, payload)
            print("✅ Webhook signature verification: OK")
            print(f"   Secret: {settings.github_webhook_secret[:10]}...")
            return True
        except Exception as e:
            print(f"❌ Webhook signature verification failed: {e}")
            return False
    except Exception as e:
        print(f"❌ Webhook signature error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_github_token():
    """Test GitHub token is set"""
    print("\n🔑 Testing GitHub Token...")
    if settings.github_token:
        print("✅ GitHub token: OK")
        print(f"   Token: {settings.github_token[:20]}...")
        return True
    else:
        print("❌ GITHUB_TOKEN not set in environment")
        return False


async def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*60)
    print("🧪 FULL PIPELINE VERIFICATION")
    print("="*60)
    
    results = {
        "health_endpoint": await test_health_endpoint(),
        "root_endpoint": await test_root_endpoint(),
        "github_token": test_github_token(),
        "webhook_signature": test_webhook_signature_verification(),
        "mongodb": await test_mongodb_connection(),
        "gemini": await test_gemini_integration(),
    }
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL SYSTEMS GO! Ready for LangGraph implementation.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Fix before proceeding.")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)
