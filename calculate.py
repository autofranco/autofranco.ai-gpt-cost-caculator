model_list = ["gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "gpt-4.5-preview",
            "gpt-4o", "gpt-4o-audio-preview", "gpt-4o-realtime-preview",
            "gpt-4o-mini", "gpt-4o-mini-audio-preview", "gpt-4o-mini-realtime-preview",
            "o1", "o1-pro", "o3", "o4-mini", "o3-mini", "o1-mini",
            "codex-mini-latest", "gpt-4o-mini-search-preview", "gpt-4o-search-preview",
            "computer-use-preview", "gpt-image-1-text", "gpt-image-1-image",
            "chatgpt-4o-latest", "gpt-4-turbo", "gpt-4", "gpt-4-32k",
            "gpt-3.5-turbo", "gpt-3.5-turbo-instruct", "gpt-3.5-turbo-16k-0613",
            "davinci-002", "babbage-002"]

token_pricing = {
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
large_model_web_search_pricing = {"low": 30, "medium": 35, "high": 50, "model":["gpt-4.1", "gpt-4o", "gpt-4o-search-preview"]}  # per 1000 calls
small_model_web_search_pricing = {"low": 25, "medium": 27.5, "high": 30, "model":["gpt-4.1-mini", "gpt-4o-mini", "gpt-4o-mini-search-preview"]}  # per 1000 calls
storage_cost_per_gb_day = 0.1  # per GB/day
file_search_cost_per_thousand_call = 2.5  # per 1000 calls

# Exchange rate (1 USD to NTD)
usd_to_ntd = 31.0
days_in_month = 30


def get_input_price_per_M(model_name):
    return token_pricing[model_name]["input"] if token_pricing.get(model_name) else 0

def get_output_price_per_M(model_name):
    return token_pricing[model_name]["output"] if token_pricing.get(model_name) else 0

def get_cached_price_per_M(model_name):
    if token_pricing.get(model_name) and token_pricing[model_name].get("cached"):
        return token_pricing[model_name]["cached"]
    else:
        return 0

def get_web_search_price_per_K(model_name, search_size):
    if search_size == "none":
        return 0
    elif large_model_web_search_pricing["model"].get(model_name):
        print("search size = ", search_size)
        print("large_model_web_search_pricing[search_size] = ", large_model_web_search_pricing[search_size])
        return large_model_web_search_pricing[search_size]
    elif small_model_web_search_pricing["model"].get(model_name):
        print("search size = ", search_size)
        print("small_model_web_search_pricing[search_size] = ", small_model_web_search_pricing[search_size])
        return small_model_web_search_pricing[search_size]
    else:
        return 0

def get_code_run_price_per_session():
    return code_interpreter_price

def get_file_search_price_per_K():
    return code_interpreter_price

def get_file_search_storage_GB_per_day(storage_size):
    if storage_size > 1:
        return storage_cost_per_gb_day * (storage_size - 1)
    else:
        return 0

def get_usd_to_ntd():
    return usd_to_ntd