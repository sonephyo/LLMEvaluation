from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

test_case = LLMTestCase(input="...", actual_output="...")
relevancy_metric = AnswerRelevancyMetric(threshold=0.5)

relevancy_metric.measure(test_case)
print(relevancy_metric.score, relevancy_metric.reason)