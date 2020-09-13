''' getReadability()
Parameters:
    URL
    - URL of site to get readability of
    - Required
    minimum_element_length
    - Minimum length of elements to include. This parameter exists to ensure english-like sentences are added to excerpt, while other html text is ignored.
    - Default: 15
    - Optional
    maximum_excerpt_length
    - Maximum length of excerpt to analyze readability of. Increasing this parameter should generally increase accuracy but runs the risk of causing 414-Request Too Large responses
    - Default: 2000
    - Optional
Outputs:
    Readability Score
    - Composite score of algorithms results
    - Allowed values 0.0 <= x <= 100.0 '''

# input: api items

import metrics
import pdb
import math

def getReadabilityDistance(user_reading_level, page_reading_level, dropoff_speed):
    x = page_reading_level - user_reading_level
    return 1*math.exp(-math.pow(x,2)/(2*dropoff_speed))

def originalIndexToRelevanceValue(index):
    return 1/(index+1)

def getWeightedRelevance(original_index, readability_distance, weight):
    weighted_relevance = 2 * (((1-weight)*originalIndexToRelevanceValue(original_index)) + (weight*readability_distance))
    return weighted_relevance

def getRelevance(api_items, user_reading_level, weight = 0.5, dropoff_speed=200):
    api_items_readability = []
    api_items_weighted_relevance = []
    api_items_word_counts = []
    for i,item in enumerate(api_items):
        api_items_word_counts.append({i:len(metrics.getExcerpt(item[i]))})
        api_items_readability.append({i:metrics.getReadability(item[i])})
        api_items_weighted_relevance.append({i:getWeightedRelevance(i,getReadabilityDistance(user_reading_level, api_items_readability[i][i], dropoff_speed),weight)})
    return api_items_weighted_relevance
