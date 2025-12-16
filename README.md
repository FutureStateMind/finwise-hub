# FinWise Hub 💰

A comprehensive personal finance management application built with Django and Vue.js. Track your bank accounts, investments, renewals, and get AI-powered financial advice to achieve financial freedom.

## Features

### 🏦 Bank Account Management
- Track multiple bank accounts (Savings, Checking, Credit Cards, Investment accounts)
- Monitor balances and account details
- Keep notes for each account

### 📊 Investment Portfolio Tracking
- Record and track various investment types (Stocks, Bonds, ETFs, Real Estate, Crypto, etc.)
- Monitor profit/loss and returns
- View investment performance metrics
- Track risk levels

### 🔄 Renewals & Subscriptions
- Track recurring payments and subscriptions
- Set renewal dates and frequencies (Daily, Weekly, Monthly, Quarterly, Yearly)
- Manage active and inactive renewals
- Monitor monthly expenses

### 🤖 AI Financial Advisor
- Comprehensive portfolio analysis
- Personalized financial recommendations
- Cash flow and liquidity analysis
- Emergency fund assessment
- Diversification analysis
- Risk profile evaluation
- Actionable task list for achieving financial freedom

### 👤 User Profile Management
- Store personal information
- Set financial goals
- Track annual income
- Secure authentication

## Technology Stack

### Backend
- **Django 6.0** - Web framework
- **Django REST Framework** - API development
- **SQLite** - Database (can be easily switched to PostgreSQL/MySQL)
- **Python 3.12+**

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vue Router** - Routing
- **Axios** - HTTP client
- **Vite** - Build tool

## Installation & Setup

### Option 1: Development Container (Recommended)

For the most consistent development experience across macOS, Linux, and Windows, use the provided development container.

#### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) or Docker Engine
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VS Code

#### Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd finwise-hub
```

2. Open in VS Code:
```bash
code .
```

3. When prompted, click "Reopen in Container" or:
   - Press `F1` (or `Ctrl+Shift+P` / `Cmd+Shift+P`)
   - Type "Dev Containers: Reopen in Container"
   - Press Enter

4. VS Code will build the container (first time only, takes a few minutes) and reopen the project inside it.

5. Once inside the container, install dependencies:

**Backend:**
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # Optional: create admin user
python manage.py runserver
```

**Frontend (in a new terminal):**
```bash
cd frontend
npm install
npm run dev
```

6. Access the application:
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:5173

#### What's Included

The development container includes:
- Ubuntu 22.04 base image
- Python 3 with pip
- Node.js 20 LTS with npm
- Git, curl, and essential build tools
- Pre-configured VS Code extensions:
  - Python and Pylance
  - Django support
  - Vue.js (Volar) and TypeScript
  - ESLint and Prettier
  - GitLens and Git Graph
  - Docker tools

#### Container Features

- **Consistent Environment**: Same development setup for all team members
- **Port Forwarding**: Automatic forwarding of ports 8000 (Django) and 5173 (Vue.js)
- **Non-root User**: Runs as `vscode` user for security
- **Persistent Storage**: Your code changes persist outside the container
- **Extension Sync**: All team members get the same VS Code extensions

### Option 2: Local Installation

If you prefer to install dependencies directly on your machine:

#### Prerequisites
- Python 3.12 or higher
- Node.js 20 or higher
- npm 10 or higher

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd finwise-hub
```


2. Install Python dependencies:
```bash
python3 -m venv finwise_env

source finwise_env/bin/activate

```

```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser (optional):
```bash
python manage.py createsuperuser
```
finwise
finwise@gmail.com
finwise@1-3rt

5. Start the Django development server:
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. **Register an Account**: Create a new user account at `/register`
2. **Login**: Access the application at `/login`
3. **Dashboard**: View your financial overview
4. **Add Bank Accounts**: Track your various bank accounts and balances
5. **Record Investments**: Add and monitor your investment portfolio
6. **Track Renewals**: Manage your subscriptions and recurring payments
7. **Get AI Advice**: Visit the AI Advisor page for personalized financial recommendations
8. **Update Profile**: Set your financial goals and personal information

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/me/` - Get current user
- `GET /api/auth/profile/` - Get user profile
- `PATCH /api/auth/profile/` - Update user profile

### Finance
- `/api/finance/bank-accounts/` - CRUD operations for bank accounts
- `/api/finance/renewals/` - CRUD operations for renewals
- `/api/finance/investments/` - CRUD operations for investments

### AI Advisor
- `GET /api/ai/analysis/` - Get full financial analysis
- `GET /api/ai/analysis/investments/` - Get investment analysis
- `GET /api/ai/analysis/cash-flow/` - Get cash flow analysis
- `GET /api/ai/recommendations/` - Get AI recommendations

## Project Structure

```
finwise-hub/
├── accounts/              # User authentication and profiles
├── finance/               # Financial data models (Bank, Investments, Renewals)
├── ai_advisor/           # AI-powered financial analysis
├── finwise_backend/      # Django project settings
├── frontend/             # Vue.js application
│   ├── src/
│   │   ├── components/  # Reusable Vue components
│   │   ├── views/       # Page components
│   │   ├── router/      # Vue Router configuration
│   │   └── services/    # API service layer
│   └── ...
├── manage.py
└── requirements.txt
```

## Key Features of AI Advisor

The AI Financial Advisor analyzes your financial data and provides:

1. **Investment Portfolio Analysis**
   - Total invested vs current value
   - Profit/loss calculations
   - Asset diversification breakdown
   - Risk profile assessment

2. **Cash Flow Analysis**
   - Total liquid cash
   - Monthly expenses estimation
   - Emergency fund coverage
   - Active subscriptions count

3. **Personalized Recommendations**
   - Prioritized by High/Medium/Low importance
   - Category-specific advice (Investment, Emergency Fund, Expenses, Savings)
   - Actionable insights based on your financial data

4. **Action Plan**
   - Step-by-step tasks to improve your financial health
   - Clear guidance for achieving financial freedom
   - Based on your specific financial situation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Future Enhancements

- Advanced charting and visualization
- Budget planning tools
- Bill payment reminders
- Integration with bank APIs
- Mobile app
- Multi-currency support
- Export reports (PDF, CSV)
- Goal tracking and milestones
- Family/shared accounts