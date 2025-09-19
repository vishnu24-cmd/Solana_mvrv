from flask import Flask, jsonify, render_template_string
from database import Database

app = Flask(__name__)

@app.route('/')
def home():
    return "Solana MVRV API Server is running!"

@app.route('/api/mvrv/latest', methods=['GET'])
def get_latest_data():
    db = Database()
    try:
        data = db.get_hourly_data(1)  # Get latest entry
        if data and len(data) > 0:
            row = data[0]
            return jsonify({
                'market_cap': float(row[2]) if row[2] is not None else 0,
                'realized_value': float(row[3]) if row[3] is not None else 0,
                'mvrv_ratio': float(row[4]) if row[4] is not None else 0,
                'circulating_supply': float(row[5]) if row[5] is not None else 0,
                'sol_price': float(row[6]) if row[6] is not None else 0,
                'timestamp': row[1].isoformat() if row[1] else None
            })
        return jsonify({'message': 'No data available yet'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/api/mvrv/hourly', methods=['GET'])
def get_hourly_data():
    db = Database()
    try:
        data = db.get_hourly_data(24)
        result = []
        for row in data:
            result.append({
                'time': row[1].isoformat() if row[1] else None,
                'market_cap': float(row[2]) if row[2] is not None else 0,
                'realized_value': float(row[3]) if row[3] is not None else 0,
                'mvrv_ratio': float(row[4]) if row[4] is not None else 0,
                'sol_price': float(row[6]) if row[6] is not None else 0
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

if __name__ == '__main__':
    print("Starting API server on http://localhost:5000")
    app.run(debug=True, port=5000)


@app.route('/dashboard')
def dashboard():
        html = """
        <!doctype html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>Solana MVRV Dashboard</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>Solana MVRV - Last 24 Hours</h1>
            <canvas id="mvrvChart" width="800" height="300"></canvas>
            <script>
                async function loadData() {
                    const resp = await fetch('/api/mvrv/hourly');
                    const data = await resp.json();
                    const labels = data.map(d=> d.time).reverse();
                    const mvrv = data.map(d=> d.mvrv_ratio).reverse();

                    const ctx = document.getElementById('mvrvChart').getContext('2d');
                    new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'MVRV Ratio',
                                data: mvrv,
                                borderColor: 'rgb(75, 192, 192)',
                                tension: 0.1
                            }]
                        }
                    });
                }
                loadData();
            </script>
        </body>
        </html>
        """
        return render_template_string(html)