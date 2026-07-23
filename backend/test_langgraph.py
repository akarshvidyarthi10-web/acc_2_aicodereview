"""
Test the multi-agent LangGraph review workflow.
"""
import asyncio
from graphs.review_graph import run_review


async def test_langgraph_review():
    """Test the LangGraph multi-agent workflow."""
    
    # Test diff with security issue, code smell, and naming issue
    test_diff = """
--- a/auth.py
+++ b/auth.py
@@ -1,10 +1,12 @@
 def login():
     u = "admin"
+    password = "secret123"
     db = get_database()
     x = db.query("SELECT * FROM users WHERE name = '" + u + "'")
     if x:
         print("logged in")
         return True
     return False

+def api_key_config():
+    return {"key": "12345"}
"""
    
    print("\n" + "="*70)
    print("🧪 TESTING MULTI-AGENT LANGGRAPH REVIEW WORKFLOW")
    print("="*70)
    
    try:
        result = await run_review(test_diff)
        
        print("\n📊 REVIEW RESULTS:")
        print(f"\n✅ Summary: {result.get('summary')}")
        print(f"🔒 Security Issues: {len(result.get('security', []))}")
        print(f"👃 Code Smells: {len(result.get('smells', []))}")
        print(f"📝 Naming Issues: {len(result.get('naming', []))}")
        print(f"⭐ Best Practice Suggestions: {len(result.get('suggestions', []))}")
        print(f"📊 Review Score: {result.get('review_score')}/100")
        print(f"📋 Recommendation: {result.get('recommendation')}")
        print(f"⏱️  Processing Time: {result.get('processing_time', 'N/A')}")
        
        # Print details
        if result.get('security'):
            print("\n🔒 Security Issues:")
            for issue in result['security']:
                print(f"   [{issue.get('severity')}] {issue.get('issue')}")
                print(f"       → {issue.get('suggestion')}")
        
        if result.get('smells'):
            print("\n👃 Code Smells:")
            for issue in result['smells']:
                print(f"   [{issue.get('severity')}] {issue.get('issue')}")
        
        if result.get('naming'):
            print("\n📝 Naming Issues:")
            for issue in result['naming']:
                print(f"   {issue.get('issue')}")
        
        if result.get('suggestions'):
            print("\n⭐ Suggestions:")
            for i, suggestion in enumerate(result['suggestions'][:3], 1):
                print(f"   {i}. {suggestion.get('issue', suggestion)}")
        
        print("\n" + "="*70)
        print("✅ LANGGRAPH WORKFLOW TEST PASSED")
        print("="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_langgraph_review())
    exit(0 if success else 1)
