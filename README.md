# tap-spoton

`tap-spoton` is a Singer tap for [SpotOn](https://www.spoton.com/), a restaurant and retail point-of-sale platform.

Built with the [Hotglue Tap SDK](https://github.com/hotgluexyz/tap-hotglue-sdk) for Singer Taps.

## Installation

```bash
pip install tap-spoton
```

Or install directly from the repository:

```bash
pip install git+https://github.com/hotgluexyz/tap-spoton.git
```

## Configuration

### Accepted Config Options

| Setting     | Required | Description                                      |
|-------------|----------|--------------------------------------------------|
| `username`  | Yes      | SpotOn API username (client ID)                  |
| `password`  | Yes      | SpotOn API password (client secret)              |
| `locations` | Yes      | Array of location IDs to sync                    |
| `start_date`| No       | The earliest record date to sync (ISO 8601 format) |

Example `config.json`:

```json
{
  "username": "your_client_id",
  "password": "your_client_secret",
  "locations": ["location_id_1", "location_id_2"],
  "start_date": "2024-01-01T00:00:00Z"
}
```

A full list of supported settings and capabilities for this tap is available by running:

```bash
tap-spoton --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

This tap uses OAuth2 client credentials authentication. You will need to obtain API credentials (username/password) from SpotOn to access their Reporting API.

## Supported Streams

| Stream      | Replication Key     | Primary Key | Description                              |
|-------------|---------------------|-------------|------------------------------------------|
| `locations` | None                | `id`        | List of configured locations             |
| `orders`    | `last_updated_at`   | `id`        | Orders with line items, payments, taxes  |

### Orders Stream Details

The `orders` stream includes comprehensive order data:

- **Line Items**: Products ordered with quantities, prices, and modifiers
- **Payments**: Payment details including type, amount, refunds, and voids
- **Totals**: Subtotal, tips, discounts, taxes, and grand total
- **Discounts**: Applied discounts with names and amounts
- **Taxes**: Tax breakdown with percentages and amounts
- **Employee**: Order ownership information
- **Metadata**: Table number, guest count, timestamps

## Usage

You can easily run `tap-spoton` by itself or in a pipeline.

### Executing the Tap Directly

```bash
tap-spoton --version
tap-spoton --help
tap-spoton --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_spoton/tests` subfolder and then run:

```bash
poetry run pytest
```

You can also test the `tap-spoton` CLI interface directly using `poetry run`:

```bash
poetry run tap-spoton --help
```
