from apify_client import ApifyClient
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env.local



# 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
def generate_response_from_domain_data(domain_data, url):
    print("Running GPT-3.5 Turbo")


    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OpenAI API key is not set in the environment variables.")

    # Initialize the OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Construct the prompt with the domain data
    prompt = f"""You are an SEO expert. Analyze the following content from the website at {url}:
    {domain_data}
    Based on the content, what keywords might the website be using for their SEO strategy?
    THE SEO keywords are used to improve page ranking on google for terms people might use to search this website or this business. All keywords are should be related to the website content.
    Please list the keywords in a JSON Format strictly. Restrict to 10 keywords"""

    # Use the OpenAI GPT model to generate a response based on the prompt

    def extract_json(data_string):
        start_index = data_string.find("{")
        end_index = data_string.rfind("}") + 1
        if start_index == -1 or end_index == 0:
            return None  # or raise an error if preferred
        return data_string[start_index:end_index]

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4-turbo",  # Adjust the model as needed
        )
        # Extract and return the generated text
        if chat_completion:
            json_part = extract_json(chat_completion.choices[0].message.content)
            return json_part
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Example usage
# if __name__ == "__main__":
#     # Assuming domain_data comes from the `analyze_domain` function or a similar source
#     domain_data = "example1.com, example2.com, example3.com"
#     print(generate_response_from_domain_data(domain_data))


def analyze_domain(url):
    # Retrieve your Apify API token from environment variables
    logging.info("Entering*******")
    api_token = os.getenv(
        "APIFY_API_TOKEN", "apify_api_YW8JJXjzU3Df8YKS3yRxUr37q0LwEe1cK6iC"
    )
    if not api_token:
        raise ValueError("API token is not set in the environment variables.")

    client = ApifyClient(api_token)

    # Prepare the Actor input with dynamic URL
    run_input = {
        "startUrls": [{"url": url}],  # Dynamic URL input
        "useSitemaps": False,
        "crawlerType": "playwright:adaptive",
        "includeUrlGlobs": [],
        "excludeUrlGlobs": [],
        "ignoreCanonicalUrl": False,
        "maxCrawlDepth": 1,
        "maxCrawlPages": 1,
        "initialConcurrency": 0,
        "maxConcurrency": 200,
        "initialCookies": [],
        "proxyConfiguration": {"useApifyProxy": True},
        "maxSessionRotations": 10,
        "maxRequestRetries": 5,
        "requestTimeoutSecs": 60,
        "minFileDownloadSpeedKBps": 128,
        "dynamicContentWaitSecs": 10,
        "maxScrollHeightPixels": 5000,
        "removeElementsCssSelector": """nav, footer, script, style, noscript, svg,
        [role="alert"],
        [role="banner"],
        [role="dialog"],
        [role="alertdialog"],
        [role="region"][aria-label*="skip" i],
        [aria-modal="true"]""",
        "removeCookieWarnings": True,
        "clickElementsCssSelector": '[aria-expanded="false"]',
        "htmlTransformer": "readableText",
        "readableTextCharThreshold": 100,
        "aggressivePrune": False,
        "debugMode": False,
        "debugLog": False,
        "saveHtml": False,
        "saveMarkdown": True,
        "saveFiles": False,
        "saveScreenshots": False,
        "maxResults": 9999999,
        "clientSideMinChangePercentage": 15,
        "renderingTypeDetectionPercentage": 10,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("aYG0l9s7dbB7j3gbS").call(run_input=run_input)
    print(f'Fetching {url}')
    # Fetch and return Actor results from the run's dataset (if there are any)
    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        if 'text' in item:
            results.append(item['text'])

    # #sample_text = f"""Revolutionizing App Business\nEmpowering Businesses Around The World\nBuilt for\nIRONSOURCE & APPLOVIN PUBLISHERS\nIncrease your ARPDAU in 21 days\nWe help publishers across the globe generate more revenue by connecting them to multiple premium DSPs & deploying cutting-edge ad optimizations with dedicated hands-on technical account management support.\nMADE FOR ADMOB PUBLISHERS (Beta)\nMaximize AdMob revenue with our data-driven automation tool!\nBoost ad revenue effortlessly with our placement automation tool. Reduce manual optimization efforts and optimize placements based on data-driven recommendations. Unlock the power of automation for greater profitability.\nGROW USERS WITH GOOGLE APP CAMPAIGN\nProfitably grow your App's User base\nScale your user base with ROI-positive campaigns that connect you to the right users. Our experts optimize your Google Ads & Facebook Ads so that you achieve the desired results with a positive ROI.\nIMPACTING APP PUBLISHERS GLOBALLY\u200b\nEmpowering the mobile app ecosystem with\n47Billion+\nAd Requests / Month\nBlogs\nWhat Are You Waiting For?\nGet in touch with our monetization experts to supercharge your app growth."""

    json_response = generate_response_from_domain_data(results,url)

    # json_response = {
    #     "result": {
    #         "keywords": ["app business", "empowering businesses", "app publishers"]
    #     }
    # }

    #     "result": "{\n  \"keywords\": [\n    \"app business\",\n    \"empowering businesses\",\n    \"ironSource publishers\",\n    \"AppLovin publishers\",\n    \"increase ARPDAU\",\n    \"premium DSPs\",\n    \"ad optimizations\",\n    \"technical account management\",\n    \"AdMob publishers\",\n    \"Maximize AdMob revenue\",\n    \"automation tool\",\n    \"placement automation\",\n    \"data-driven recommendations\",\n    \"Google App Campaign\",\n    \"grow user base\",\n    \"ROI-positive campaigns\",\n    \"Google Ads optimization\",\n    \"Facebook Ads optimization\",\n    \"app publishers\",\n    \"mobile app ecosystem\",\n    \"ad requests\",\n    \"monetization experts\",\n    \"app growth\"\n  ]\n}"
    # }
    print("Returning JSON")
    return json_response


# Updates credit value as well
def insert_result_into_db(result, user_id, domain, credits, supabase):
    response = (
        supabase.table("QueryResultDB")
        .insert({"user_id": user_id, "query": domain, "query_result": result})
        .execute()
    )
    logging.debug(response)
    response = (
        supabase.table("UserDB")
        .update({"credits": credits - 1})
        .eq("user_id", user_id)
        .execute()
    )
    logging.debug(response)
