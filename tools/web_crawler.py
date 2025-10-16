import time
import warnings
from typing import ClassVar

import selenium
from pydantic import BaseModel, Field
from google.adk.tools.load_artifacts_tool import load_artifacts_tool
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from PIL import Image
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from util import constants
from beeai_framework.context import RunContext
from beeai_framework.emitter import Emitter
from beeai_framework.tools import StringToolOutput, Tool, ToolRunOptions

warnings.filterwarnings("ignore", category=UserWarning)

class WebCrawlSchema(BaseModel):
    crawl: str = Field(..., description="This helps crawl in any website and share details.")

class CrawlInput(BaseModel):
    url: str
    x: int
    y: int
    text: str
    text_to_enter: str
    element_id: str
    page_source: str
    user_task: str

class WebCrawlTool(Tool):
    name: ClassVar[str]= "crawl_web"
    description : ClassVar[str]= "Crawl through any website being asked for and share the insights" 
    input_schema = CrawlInput

    def __init__(self, *, extra_instructions: str = "") -> None:
        super().__init__()
        if extra_instructions:
            self.description += f" {extra_instructions}"

    @property
    def input_schema(self) -> type[CrawlInput]:
        return CrawlInput

    async def _run(self, input: CrawlInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        return StringToolOutput("OK")

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "crawl_web"],
            creator=self,
        )

if not constants.DISABLE_WEB_DRIVER:
    options = Options()
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--verbose")
    options.add_argument("--headless=new")  # Use new headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = selenium.webdriver.Chrome(options=options)

class GoToURLTool(Tool):
    name: ClassVar[str]= "go_to_url"
    description : ClassVar[str]= "Navigates the browser to the given URL." 
    input_schema = CrawlInput

    # def run(self, input: CrawlInput) -> str:
    #     """Navigates the browser to the given URL."""
    #     print(f"🌐 Navigating to URL: {input.url}")  # Added print statement
    #     driver.get(input.url)
    #     return f"Navigated to URL: {input.url}"

    def __init__(self, *, extra_instructions: str = "") -> None:
        super().__init__()
        if extra_instructions:
            self.description += f" {extra_instructions}"

    @property
    def input_schema(self) -> type[CrawlInput]:
        return CrawlInput

    async def _run(self, input: CrawlInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Navigates the browser to the given URL."""
        print(f"🌐 Navigating to URL: {input.url}")  # Added print statement
        driver.get(input.url)
        return f"Navigated to URL: {input.url}"
 
    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "go_to_url"],
            creator=self,
        )

class ClickAtCoordinates(Tool):
    name: ClassVar[str]= "click_at_coordinates"
    description : ClassVar[str]= "Clicks at the specified coordinates on the screen." 
    input_schema = CrawlInput

    # def run(self, x: int, y: int) -> str:
    #     """Clicks at the specified coordinates on the screen."""
    #     driver.execute_script(f"window.scrollTo({x}, {y});")
    #     driver.find_element(By.TAG_NAME, "body").click()

    def __init__(self, *, extra_instructions: str = "") -> None:
        super().__init__()
        if extra_instructions:
            self.description += f" {extra_instructions}"

    @property
    def input_schema(self) -> type[CrawlInput]:
        return CrawlInput

    async def _run(self, input: CrawlInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Clicks at the specified coordinates on the screen."""
        driver.execute_script(f"window.scrollTo({input.x}, {input.y});")
        driver.find_element(By.TAG_NAME, "body").click()

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "click_at_coordinates"],
            creator=self,
        )

class FindElementWithText(Tool[WebCrawlSchema]):
    name: ClassVar[str]= "find_element_with_text"
    description : ClassVar[str]= "Finds an element on the page with the given text." 
    input_schema = CrawlInput

    # def run(self, text: str) -> str:
    #     """Finds an element on the page with the given text."""
    #     print(f"🔍 Finding element with text: '{text}'")  # Added print statement

    #     try:
    #         element = driver.find_element(By.XPATH, f"//*[text()='{text}']")
    #         if element:
    #             return "Element found."
    #         else:
    #             return "Element not found."
    #     except selenium.common.exceptions.NoSuchElementException:
    #         return "Element not found."
    #     except selenium.common.exceptions.ElementNotInteractableException:
    #         return "Element not interactable, cannot click."

    def __init__(self, *, extra_instructions: str = "") -> None:
        super().__init__()
        if extra_instructions:
            self.description += f" {extra_instructions}"

    @property
    def input_schema(self) -> type[CrawlInput]:
        return CrawlInput

    async def _run(self, input: CrawlInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Finds an element on the page with the given text."""
        print(f"🔍 Finding element with text: '{input.text}'")  # Added print statement

        try:
            element = driver.find_element(By.XPATH, f"//*[text()='{input.text}']")
            if element:
                return "Element found."
            else:
                return "Element not found."
        except selenium.common.exceptions.NoSuchElementException:
            return "Element not found."
        except selenium.common.exceptions.ElementNotInteractableException:
            return "Element not interactable, cannot click."

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "find_element_with_text"],
            creator=self,
        )

class ClickElementWithText(Tool[WebCrawlSchema]):
    name: ClassVar[str]= "click_element_with_text"
    description : ClassVar[str]= "Clicks on an element on the page with the given text." 
    input_schema = CrawlInput

    def __init__(self, *, extra_instructions: str = "") -> None:
        super().__init__()
        if extra_instructions:
            self.description += f" {extra_instructions}"

    @property
    def input_schema(self) -> type[CrawlInput]:
        return CrawlInput

    async def _run(self, input: CrawlInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Clicks on an element on the page with the given text."""
        print(f"🖱️ Clicking element with text: '{input.text}'")  # Added print statement

        try:
            element = driver.find_element(By.XPATH, f"//*[text()='{input.text}']")
            element.click()
            return f"Clicked element with text: {input.text}"
        except selenium.common.exceptions.NoSuchElementException:
            return "Element not found, cannot click."
        except selenium.common.exceptions.ElementNotInteractableException:
            return "Element not interactable, cannot click."
        except selenium.common.exceptions.ElementClickInterceptedException:
            return "Element click intercepted, cannot click."

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "click_element_with_text"],
            creator=self,
        )

class EnterTextIntoElement(Tool[WebCrawlSchema]):
    name: ClassVar[str]= "enter_text_into_element"
    description : ClassVar[str]= "Enters text into an element with the given ID." 
    input_schema = CrawlInput

    def __init__(self, *, extra_instructions: str = "") -> None:
        super().__init__()
        if extra_instructions:
            self.description += f" {extra_instructions}"

    @property
    def input_schema(self) -> type[CrawlInput]:
        return CrawlInput

    async def _run(self, input: CrawlInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Enters text into an element with the given ID."""
        print(
            f"📝 Entering text '{input.text_to_enter}' into element with ID: {input.element_id}"
        )  # Added print statement

        try:
            input_element = driver.find_element(By.ID, input.element_id)
            input_element.send_keys(input.text_to_enter)
            return (
                f"Entered text '{input.text_to_enter}' into element with ID: {input.element_id}"
            )
        except selenium.common.exceptions.NoSuchElementException:
            return "Element with given ID not found."
        except selenium.common.exceptions.ElementNotInteractableException:
            return "Element not interactable, cannot click."
    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "enter_text_into_element"],
            creator=self,
        )

class ScrollDownScreen(Tool):

    name: ClassVar[str]= "scroll_down_screen"
    description : ClassVar[str]= "Scrolls down the screen by a moderate amount." 
    input_schema = CrawlInput

    def __init__(self, *, extra_instructions: str = "") -> None:
        super().__init__()
        if extra_instructions:
            self.description += f" {extra_instructions}"

    @property
    def input_schema(self) -> type[CrawlInput]:
        return CrawlInput

    async def _run(self, input: CrawlInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Scrolls down the screen by a moderate amount."""
        print("⬇️ scroll the screen")  # Added print statement
        driver.execute_script("window.scrollBy(0, 500)")
        return "Scrolled down the screen."

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "scroll_down_screen"],
            creator=self,
        )

class GetPageSource(Tool):

    name: ClassVar[str]= "get_page_source"
    description : ClassVar[str]= "Returns the current page source." 
    input_schema = CrawlInput

    def __init__(self, *, extra_instructions: str = "") -> None:
        super().__init__()
        if extra_instructions:
            self.description += f" {extra_instructions}"

    @property
    def input_schema(self) -> type[CrawlInput]:
        return CrawlInput

    async def _run(self, input: CrawlInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        LIMIT = 1000000
        """Returns the current page source."""
        print("📄 Getting page source...")  # Added print statement
        return driver.page_source[0:LIMIT]

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "get_page_source"],
            creator=self,
        )

class AnalyzeWebpagAndDetermineAction(Tool):
    name: ClassVar[str]= "analyze_webpage_and_determine_action"
    description : ClassVar[str]= "Analyzes the webpage and determines the next action (scroll, click, etc.)." 
    input_schema = CrawlInput

    def __init__(self, *, extra_instructions: str = "") -> None:
        super().__init__()
        if extra_instructions:
            self.description += f" {extra_instructions}"

    @property
    def input_schema(self) -> type[CrawlInput]:
        return CrawlInput

    async def _run(self, input: CrawlInput, options: ToolRunOptions | None, context: RunContext) -> StringToolOutput:
        """Analyzes the webpage and determines the next action (scroll, click, etc.)."""
        print(
            "🤔 Analyzing webpage and determining next action..."
        )  # Added print statement

        analysis_prompt = f"""
        You are an expert web page analyzer.
        You have been tasked with controlling a web browser to achieve a user's goal.
        The user's task is: {input.user_task}
        Here is the current HTML source code of the webpage:
        ```html
        {input.page_source}
        ```

        Based on the webpage content and the user's task, determine the next best action to take.
        Consider actions like: completing page source, scrolling down to see more content, clicking on links or buttons to navigate, or entering text into input fields.

        Think step-by-step:
        1. Briefly analyze the user's task and the webpage content.
        2. If source code appears to be incomplete, complete it to make it valid html. Keep the product titles as is. Only complete missing html syntax
        3. Identify potential interactive elements on the page (links, buttons, input fields, etc.).
        4. Determine if scrolling is necessary to reveal more content.
        5. Decide on the most logical next action to progress towards completing the user's task.

        Your response should be a concise action plan, choosing from these options:
        - "COMPLETE_PAGE_SOURCE": If source code appears to be incomplete, complte it to make it valid html
        - "SCROLL_DOWN": If more content needs to be loaded by scrolling.
        - "CLICK: <element_text>": If a specific element with text <element_text> should be clicked. Replace <element_text> with the actual text of the element.
        - "ENTER_TEXT: <element_id>, <text_to_enter>": If text needs to be entered into an input field. Replace <element_id> with the ID of the input element and <text_to_enter> with the text to enter.
        - "TASK_COMPLETED": If you believe the user's task is likely completed on this page.
        - "STUCK": If you are unsure what to do next or cannot progress further.
        - "ASK_USER": If you need clarification from the user on what to do next.

        If you choose "CLICK" or "ENTER_TEXT", ensure the element text or ID is clearly identifiable from the webpage source. If multiple similar elements exist, choose the most relevant one based on the user's task.
        If you are unsure, or if none of the above actions seem appropriate, default to "ASK_USER".

        Example Responses:
        - SCROLL_DOWN
        - CLICK: Learn more
        - ENTER_TEXT: search_box_id, Gemini API
        - TASK_COMPLETED
        - STUCK
        - ASK_USER

        What is your action plan?
        """
        return analysis_prompt

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "analyze_webpage_and_determine_action"],
            creator=self,
        )

## Web crawler