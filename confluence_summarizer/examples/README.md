# Confluence Summarizer Examples

This directory contains example notebooks demonstrating how to use the Confluence Summarizer tool.

## Getting Started

1. Install the required dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

2. Set up your environment variables:
   ```bash
   export AZURE_OPENAI_API_KEY="your-api-key"
   export AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment-name"
   export AZURE_OPENAI_ENDPOINT="your-endpoint-url"
   export CONFLUENCE_URL="https://your-domain.atlassian.net"
   export CONFLUENCE_USERNAME="your-email@example.com"
   export CONFLUENCE_API_TOKEN="your-api-token"
   export CONFLUENCE_SPACE_KEY="TEAM"
   ```

3. Start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

4. Open `confluence_summarizer_examples.ipynb`

## Example Notebooks

### confluence_summarizer_examples.ipynb

This notebook contains seven comprehensive examples:

1. **Basic Summary Generation**
   - Simple example of generating a summary
   - Displaying metadata and results

2. **Technical Summary with Context**
   - Generating a technical-focused summary
   - Using specific context for implementation details
   - Including child pages

3. **Business-Focused Summary**
   - Creating a business-oriented summary
   - Focusing on objectives and ROI
   - Excluding child pages for conciseness

4. **Comparing Summaries**
   - Generating different types of summaries
   - Comparing technical vs. business summaries
   - Displaying differences and statistics

5. **Tracking Changes Over Time**
   - Demonstrating how to track page changes
   - Comparing summaries from different times
   - Showing metadata and content differences

6. **Custom Persona Summary**
   - Creating a security-focused persona
   - Generating specialized summaries
   - Using custom context

7. **Batch Processing Multiple Pages**
   - Processing multiple pages in sequence
   - Error handling for batch operations
   - Displaying results for each page

## Running the Examples

1. Make sure you have the correct Confluence page IDs for your space
2. Update the page IDs in the examples with your actual page IDs
3. Run each cell in sequence to see the results
4. Check the exported markdown files in the `summaries` directory

## Notes

- The examples use placeholder page IDs (e.g., "123456"). Replace these with actual page IDs from your Confluence space.
- Some examples may take longer to run due to API calls and content processing.
- The exported summaries are saved in the `summaries` directory by default.
- Make sure you have sufficient permissions to access the Confluence pages.

## Troubleshooting

If you encounter any issues:

1. Verify your environment variables are set correctly
2. Check your Confluence API token and permissions
3. Ensure your Azure OpenAI configuration is correct
4. Check the network connection to both Confluence and Azure OpenAI
5. Look for error messages in the notebook output

## Contributing

Feel free to add more examples or modify the existing ones. When adding new examples:

1. Follow the existing format and style
2. Include clear markdown explanations
3. Add error handling
4. Document any assumptions or requirements
5. Test the example with real Confluence pages 