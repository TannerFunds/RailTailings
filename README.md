# TailingsIQ - Railway Optimized Version

## Overview

This is a Railway-optimized version of the TailingsIQ tailings management system, designed for easy deployment by non-developers. The application has been restructured with stable dependencies and simplified configuration.

## Project Structure

```
tailingsiq-railway/
├── backend/                 # FastAPI backend service
│   ├── main.py             # Main API application
│   ├── requirements.txt    # Python dependencies (stable versions)
│   ├── Procfile           # Railway process configuration
│   └── .env.example       # Environment variables template
├── frontend/              # React frontend application
│   ├── src/               # Source code
│   ├── package.json       # Node.js dependencies
│   └── .env.example       # Frontend environment template
└── README.md              # This file
```

## Key Improvements for Railway Deployment

### Backend Optimizations
- **Stable Dependencies**: Using tested, stable versions of all packages
- **Simplified Architecture**: Removed complex AWS dependencies
- **Railway Configuration**: Added Procfile and proper port handling
- **Environment Variables**: Clear configuration for Railway deployment
- **Database Ready**: MongoDB integration with connection string support

### Frontend Optimizations
- **Modern React**: Built with Vite for fast builds and development
- **UI Components**: Professional interface using shadcn/ui components
- **Responsive Design**: Works on desktop and mobile devices
- **API Integration**: Configured to connect to Railway backend
- **Environment Configuration**: Easy API URL configuration

## Features

### Backend API Features
- **Authentication**: Simple token-based authentication
- **Facility Management**: CRUD operations for tailings facilities
- **Document Management**: Upload and manage facility documents
- **Monitoring Data**: Real-time sensor data collection
- **Risk Assessment**: AI-powered risk analysis (simplified for demo)
- **Health Checks**: Railway-compatible health monitoring

### Frontend Features
- **Dashboard**: Overview of system status and metrics
- **Facility Management**: Visual interface for managing facilities
- **Real-time Monitoring**: Live sensor data display
- **Risk Assessment**: Interactive risk analysis tools
- **Reports**: Generated analytics and recommendations
- **Responsive Design**: Mobile-friendly interface

## Quick Start

### Local Development

1. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   python main.py
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   pnpm install
   cp .env.example .env
   # Edit .env with backend URL
   pnpm run dev
   ```

### Railway Deployment

1. **Prepare Repository**:
   - Upload this entire `tailingsiq-railway` folder to GitHub
   - Ensure both backend and frontend folders are included

2. **Deploy Backend**:
   - Create new Railway project
   - Connect GitHub repository
   - Select backend folder as service root
   - Add environment variables (see Backend Environment Variables below)
   - Railway will automatically detect Python and deploy

3. **Deploy Frontend**:
   - Add new service to same Railway project
   - Connect same GitHub repository
   - Select frontend folder as service root
   - Set VITE_API_URL to backend service URL
   - Railway will automatically detect Node.js and deploy

## Environment Variables

### Backend Environment Variables (Required)
Set these in Railway dashboard for your backend service:

```
MONGODB_URI=your_mongodb_connection_string
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_here
```

### Frontend Environment Variables (Required)
Set these in Railway dashboard for your frontend service:

```
VITE_API_URL=https://your-backend-service.railway.app
```

## Database Setup

### Option 1: Railway MongoDB (Recommended)
1. Add MongoDB service to your Railway project
2. Copy the connection string from Railway dashboard
3. Set MONGODB_URI environment variable in backend service

### Option 2: External MongoDB
1. Use MongoDB Atlas (free tier available)
2. Create cluster and get connection string
3. Set MONGODB_URI environment variable in backend service

## API Keys Setup

### OpenAI API Key
1. Sign up at [OpenAI](https://openai.com)
2. Generate API key in dashboard
3. Set OPENAI_API_KEY environment variable

### Anthropic API Key (Optional)
1. Sign up at [Anthropic](https://anthropic.com)
2. Generate API key in dashboard
3. Set ANTHROPIC_API_KEY environment variable

## Testing

### Demo Credentials
- Username: `demo`
- Password: `demo`

### API Endpoints
- Health Check: `GET /health`
- API Documentation: `GET /docs`
- Authentication: `POST /token`
- Facilities: `GET /facilities`

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check that requirements.txt has correct package versions
   - Ensure Python version compatibility (3.8+)
   - Verify all environment variables are set

2. **Connection Issues**:
   - Verify VITE_API_URL points to correct backend URL
   - Check CORS settings in backend
   - Ensure MongoDB connection string is correct

3. **Authentication Issues**:
   - Use demo credentials: demo/demo
   - Check that JWT_SECRET_KEY is set
   - Verify token is being stored in localStorage

### Railway-Specific Tips

1. **Port Configuration**: Railway automatically sets PORT environment variable
2. **Domain Generation**: Use Railway's domain generation for public URLs
3. **Environment Variables**: Set in Railway dashboard, not in code
4. **Logs**: Check Railway deployment logs for detailed error information

## Production Considerations

### Security
- Change default demo credentials
- Use strong JWT secret keys
- Implement proper user authentication
- Enable HTTPS (Railway provides this automatically)

### Performance
- Consider database indexing for large datasets
- Implement caching for frequently accessed data
- Monitor resource usage in Railway dashboard

### Monitoring
- Set up Railway alerts for service health
- Implement application-level logging
- Monitor API response times and error rates

## Support

For deployment issues:
1. Check Railway documentation
2. Review deployment logs in Railway dashboard
3. Verify all environment variables are correctly set
4. Test API endpoints using the /docs interface

## Version Information

- **Backend**: FastAPI 0.104.1, Python 3.8+
- **Frontend**: React 19.1.0, Vite 6.3.5
- **Database**: MongoDB (any recent version)
- **Deployment**: Railway Platform

This optimized version addresses common deployment issues and provides a stable foundation for the TailingsIQ application.

