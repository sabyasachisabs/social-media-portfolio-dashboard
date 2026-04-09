#!/usr/bin/env python3
"""Test Supabase connection"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_supabase_connection():
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        print("❌ Error: SUPABASE_URL or SUPABASE_KEY not found in environment variables")
        return False

    print(f"✅ Found SUPABASE_URL: {supabase_url[:30]}...")
    print(f"✅ Found SUPABASE_KEY: {supabase_key[:20]}...")

    try:
        from supabase import create_client
        client = create_client(supabase_url, supabase_key)
        print("✅ Supabase client created successfully")

        # Test connection by trying to select from the table
        response = client.table("social_posts").select("*").limit(1).execute()
        print("✅ Successfully connected to Supabase and queried table")
        print(f"Response type: {type(response)}")

        # Check for error attribute
        if hasattr(response, 'error'):
            print(f"Error attribute: {response.error}")
            if response.error:
                print(f"❌ Response error: {response.error}")
                return False
        else:
            print("No error attribute found")

        if hasattr(response, 'data'):
            data = response.data
            print(f"✅ Response data type: {type(data)}")
            if data:
                print(f"✅ Found {len(data)} records in the table")
                print(f"Sample record: {data[0] if data else 'None'}")
            else:
                print("ℹ️  Table exists but is empty")
        else:
            print("❌ No data attribute in response")

        # Test inserting sample data
        print("\n--- Testing data insertion ---")
        sample_data = {
            "project_id": "TEST001",
            "project_name": "Test Project",
            "platform": "LinkedIn",
            "post_url": "https://linkedin.com/test",
            "post_date": "2024-01-01",
            "likes": 10,
            "comments": 5,
            "impressions": 100
        }

        insert_response = client.table("social_posts").insert(sample_data).execute()
        print("✅ Sample data inserted successfully")
        print(f"Insert response data: {insert_response.data}")

        # Clean up - delete the test record
        if insert_response.data and len(insert_response.data) > 0:
            record_id = insert_response.data[0]['id']
            delete_response = client.table("social_posts").delete().eq('id', record_id).execute()
            print("✅ Test record cleaned up")

        return True

    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_supabase_connection()