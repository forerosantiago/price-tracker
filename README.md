# price-tracker

## To run locally
1. Ensure you have Python installed (version 3.6 or higher).
2. Clone the repository.
    ```bash
   git clone https://github.com/forerosantiago/price-tracker
    ```
3. Navigate to the project directory.
   ```bash
   cd price-tracker
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the main script:
   ```bash
   python main.py
   ```

## To run in Docker
1. `git clone https://github.com/forerosantiago/price-tracker`
2. `cd price-tracker`
3. `docker build -t price-tracker .`
4. `docker run -it --rm price-tracker`