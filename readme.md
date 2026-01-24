# scoPy
Python project for pointing my telescope.

## Setup and Virtual Environment
1. Create a virtual environment (recommended):

	 ```sh
	 python3 -m venv .venv
	 ```

2. Activate the virtual environment:

	 - On macOS/Linux:
		 ```sh
		 source .venv/bin/activate
		 ```
	 - On Windows:
		 ```sh
		 .venv\Scripts\activate
		 ```

3. Install dependencies:

	```sh
	pip install -r requirements.txt
	```

4. To deactivate the virtual environment when done:

	```sh
	deactivate
	```

5. In order to register packages as being present in Visual Studio Code, you should do the following:
<ol>
	<li>Open the Command Palette (⇧⌘P or Ctrl+Shift+P).</li>
	<li>Type and select “Python: Select Interpreter.”</li>
	<li>Choose the interpreter that points to your project’s .venv (it will look like .venv/bin/python or similar).</li>
</ol>

## Running Tests Locally
Run the following command to run the unit tests in a docker container:
```sh
docker compose up --build
```

