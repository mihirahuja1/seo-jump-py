def check_user_credits(user_id, supabase):
    response = (
        supabase.table("UserDB").select("credits").eq("user_id", user_id).execute()
    )
    credits = response.data[0]["credits"] if response.data else 0
    return True if credits >= 1 else False, credits
