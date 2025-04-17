Follow complete documentation on www.evehwang.com

## Executive Summary

‘Item Backfill for Weight and Dimensions’ creates an AI-powered solution that predicts missing weight and dimensional data for products in supply chain operations. 

Using Claude, Anthropic's large language model, the system analyzes product descriptions to generate accurate estimations of physical attributes when this information is missing from vendor data. 

This solution addresses a critical operational gap in supply chain management, reducing operating costs and improving planning accuracy across transportation, warehousing, and order fulfillment processes. 

## Scope

This project is a training exercise in agentic automation within a supply chain context, intended to demonstrate the technical feasibility and business potential of using generative AI to solve supply chain data problems. It includes the development of a working prototype that can accurately predict weight and dimensional data for a limited set of SKUs from their descriptions. 

- The project will remain within the domain expertise boundaries expected of a Product Manager, emphasizing conceptual validation rather than full-scale implementation.
- Development will occur with minimal overhead costs, using freely available or trial versions of necessary tools.
- The dataset will be intentionally constrained to a representative sample size sufficient to demonstrate efficacy across various product categories.

The project will be considered complete and successful upon delivery of a viable prototype that demonstrates the approach works within defined accuracy thresholds, along with comprehensive documentation of the methodology, results, and projected cost analysis for a potential production implementation.

## Problem Statement

Incomplete product data, specifically missing weight and dimension information, represents a significant challenge for supply chain organizations. When retailers acquire products from vendors, they may not receive incomplete documentation, creating cascading problems throughout the supply chain:

- Transportation planning becomes inefficient without accurate weight and volume calculations, leading to underutilized or overloaded shipments.
- Warehouse operations suffer from improper space allocation and storage planning.
- Order fulfillment experiences delays and errors when packaging decisions must be made without proper dimensional data.
- Manual research to backfill this information is time-consuming, expensive, and often delayed until the physical product arrives, creating bottlenecks in the supply chain.

The cumulative effect of these inefficiencies results in higher operational costs, increased delivery times, and reduced customer satisfaction.

## Solution Approach

The project proposes an agentic AI system to predict missing weight and dimension data based on product descriptions and classifications. Agentic AI systems are artificial intelligence applications that autonomously complete specific tasks, using goal-directed behavior to make context-aware decisions. 

The solution architecture used for this project will include connecting data sources to Claude to analyze product descriptions, and make intelligent predictions about physical attributes. The agent will rely solely on Claude's existing knowledge of products and their typical dimensions, and the possibility of adding a RAG to improve results will be investigated. 

## Key Outcomes and Results

This proof-of-concept project aims to deliver several specific and measurable outcomes:

- A functional end-to-end system capable of processing SKU descriptions and generating predicted weight and dimensional data with quantifiable accuracy.
- Evaluation of accuracy, to measure overall correctness of predictions within acceptable tolerances
- Evaluation of precision, to evaluate the reliability of positive predictions (when dimensions are deemed within usable ranges)
- Evaluation of recall, to assess the system's ability to identify all products for which accurate predictions can be made
- A confidence matrix to support assessing prediction accuracy
- Documentation of credit costs to inform savings compared to manual research methods.

Full ROI analysis is out of scope. However, success in the stated Key Outcomes will indicate whether resourcing ought to be provided to estimate labor savings and other opportunities in transportation planning, warehouse space optimization, and shipping cost reduction.