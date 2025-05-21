def run(daily_interactions, model_name, input_tokens, output_tokens, cached_tokens, web_search_content_size, code_interpreter_used, file_search_storage):
    # Pricing table for GPT models (in USD per 1,000,000 tokens)
    pricing = {
        "gpt-4.1": {"input": 2.00, "cached": 0.50, "output": 8.00},
        "gpt-4.1-mini": {"input": 0.40, "cached": 0.10, "output": 1.60},
        "gpt-4.1-nano": {"input": 0.10, "cached": 0.025, "output": 0.40},
        "gpt-4.5-preview": {"input": 75.00, "cached": 37.50, "output": 150.00},
        "gpt-4o": {"input": 2.50, "cached": 1.25, "output": 10.00},
        "gpt-4o-audio-preview": {"input": 2.50, "cached": None, "output": 10.00},
        "gpt-4o-realtime-preview": {"input": 5.00, "cached": 2.50, "output": 20.00},
        "gpt-4o-mini": {"input": 0.15, "cached": 0.075, "output": 0.60},
        "gpt-4o-mini-audio-preview": {"input": 0.15, "cached": None, "output": 0.60},
        "gpt-4o-mini-realtime-preview": {"input": 0.60, "cached": 0.30, "output": 2.40},
        "o1": {"input": 15.00, "cached": 7.50, "output": 60.00},
        "o1-pro": {"input": 150.00, "cached": None, "output": 600.00},
        "o3": {"input": 10.00, "cached": 2.50, "output": 40.00},
        "o4-mini": {"input": 1.10, "cached": 0.275, "output": 4.40},
        "o3-mini": {"input": 1.10, "cached": 0.55, "output": 4.40},
        "o1-mini": {"input": 1.10, "cached": 0.55, "output": 4.40},
        "codex-mini-latest": {"input": 1.50, "cached": 0.375, "output": 6.00},
        "gpt-4o-mini-search-preview": {"input": 0.15, "cached": None, "output": 0.60},
        "gpt-4o-search-preview": {"input": 2.50, "cached": None, "output": 10.00},
        "computer-use-preview": {"input": 3.00, "cached": None, "output": 12.00},
        "gpt-image-1-text": {"input": 5.00, "cached": None, "output": None},
        "gpt-image-1-image": {"input": 10.00, "cached": None, "output": 40.00},
        "chatgpt-4o-latest": {"input": 5.00, "output": 15.00},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-4": {"input": 30.00, "output": 60.00},
        "gpt-4-32k": {"input": 60.00, "output": 120.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        "gpt-3.5-turbo-instruct": {"input": 1.50, "output": 2.00},
        "gpt-3.5-turbo-16k-0613": {"input": 3.00, "output": 4.00},
        "davinci-002": {"input": 2.00, "output": 2.00},
        "babbage-002": {"input": 0.40, "output": 0.40}
    }
    
    code_interpreter_price = 0.03  # per session
    large_model_web_search_pricing = {"low": 30, "medium": 35, "high": 50}  # per 1000 calls
    small_model_web_search_pricing = {"low": 25, "medium": 27.5, "high": 30}  # per 1000 calls
    storage_cost_per_gb_day = 0.1  # per GB/day
    file_search_cost_per_thousand_call = 2.5  # per 1000 calls
    
    # Exchange rate (1 USD to NTD)
    usd_to_ntd = 31.0
    days_in_month = 30
    
    
    monthly_input_tokens = daily_interactions * input_tokens * days_in_month
    monthly_output_tokens = daily_interactions * output_tokens * days_in_month
    monthly_cached_tokens = daily_interactions * cached_tokens * days_in_month
    
    if model_name not in pricing:
        print({"error": f"Pricing information not available for model {model_name}"})
        return {"error": f"Pricing information not available for model {model_name}"}
    
    model_pricing = pricing[model_name]
    
    input_cost_usd = (monthly_input_tokens / 1_000_000) * (model_pricing["input"] or 0)
    output_cost_usd = (monthly_output_tokens / 1_000_000) * (model_pricing["output"] or 0)
    cached_cost_usd = (monthly_cached_tokens / 1_000_000) * (model_pricing["cached"] or 0)
    
    # Web search cost
    web_search_cost = 0
    if web_search_content_size != "none":
        if model_name in ["gpt-4.1", "4o", "gpt-4o-search-preview"]:
            # Use large model pricing  # "none", low", "medium", "high"
            web_search_cost = (daily_interactions / 1000) * large_model_web_search_pricing.get(web_search_content_size, 0)
        elif model_name in ["gpt-4.1-mini", "4o-mini", "gpt-4o-mini-search-preview"]:
            web_search_cost = (daily_interactions / 1000) * small_model_web_search_pricing.get(web_search_content_size, 0)
    
    # File search cost
    file_search_storage_cost = file_search_storage * storage_cost_per_gb_day * 30 if file_search_storage > 1 else 0
    file_search_tool_call_cost = (daily_interactions / 1000) * file_search_cost_per_thousand_call * 30 if file_search_storage > 1 else 0
    file_search_cost = file_search_storage_cost + file_search_tool_call_cost
    
    # Code interpreter cost
    code_interpreter_cost = 0
    if code_interpreter_used:
        code_interpreter_cost = daily_interactions * code_interpreter_price
    
    # total cost
    total_cost_usd = input_cost_usd + output_cost_usd + cached_cost_usd + web_search_cost + file_search_cost + code_interpreter_cost
    total_cost_ntd = total_cost_usd * usd_to_ntd
    
    # result
    result = {
        "model_name": model_name,
        "monthly_input_tokens": monthly_input_tokens,
        "monthly_output_tokens": monthly_output_tokens,
        "monthly_cached_tokens": monthly_cached_tokens,
        "input_cost_usd": round(input_cost_usd, 2),
        "output_cost_usd": round(output_cost_usd, 2),
        "cached_cost_usd": round(cached_cost_usd, 2),
        "web_search_cost": round(web_search_cost, 2),
        "file_search_cost": round(file_search_cost, 2),
        "code_interpreter_cost": round(code_interpreter_cost, 2),
        "total_cost_usd": round(total_cost_usd, 2),
        "total_cost_ntd": round(total_cost_ntd, 2)
    }
    for key, value in result.items():
        print(f"{key}: {value}")
    return result
# run(daily_interactions, model_name, input_tokens, output_tokens, cached_tokens, web_search_content_size, code_interpreter_used, file_search_storage)