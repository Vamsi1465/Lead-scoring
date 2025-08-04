import pandas as pd
import json

def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def score_lead(row, config):
    score = 0

    # Job title score
    job_score = config["job_title_scores"].get(row["job_title"], 0)
    score += job_score

    # Location score
    location_score = config["location_scores"].get(row["location"], 0)
    score += location_score

    # Interactions score
    interactions = row["interactions"]
    interaction_thresholds = config["thresholds"]["interactions"]
    if interactions >= interaction_thresholds["high"]:
        score += 3
    elif interactions >= interaction_thresholds["medium"]:
        score += 2
    else:
        score += 1

    # Page views score
    views = row["page_views"]
    view_thresholds = config["thresholds"]["page_views"]
    if views >= view_thresholds["high"]:
        score += 3
    elif views >= view_thresholds["medium"]:
        score += 2
    else:
        score += 1

    return score

def main():
    config = load_config('config.json')
    df = pd.read_csv('sample_leads.csv')

    df['lead_score'] = df.apply(lambda row: score_lead(row, config), axis=1)

    # Optional: categorize leads
    def categorize(score):
        if score >= 8:
            return 'Hot'
        elif score >= 5:
            return 'Warm'
        else:
            return 'Cold'

    df['lead_category'] = df['lead_score'].apply(categorize)

    df.to_csv('scored_leads.csv', index=False)
    print("✅ Lead scoring complete. Results saved to 'scored_leads.csv'.")

if __name__ == '__main__':
    main()
