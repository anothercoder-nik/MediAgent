# Railway Deployment Guide for Medical Diagnostics API

## Prerequisites
- Railway account (sign up at [railway.app](https://railway.app))
- Git repository with your code
- OpenAI/OpenRouter API key

## Deployment Steps

### 1. Prepare Your Repository
Make sure all these files are in your repository:
- `app.py` (main Flask application)
- `Procfile` (Railway process configuration)
- `requirements_api.txt` (Python dependencies)
- `railway.json` (Railway configuration)
- `runtime.txt` (Python version specification)
- `Utils/Agents.py` (agent classes and PDF generation)

### 2. Deploy to Railway

#### Option A: Deploy from GitHub
1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account and select this repository
5. Railway will automatically detect the Python app and start deployment

#### Option B: Deploy from Command Line
1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```
2. Login to Railway:
   ```bash
   railway login
   ```
3. Initialize project:
   ```bash
   railway init
   ```
4. Deploy:
   ```bash
   railway up
   ```

### 3. Set Environment Variables
In Railway dashboard, go to your project → Variables tab and add:

**Required Variables:**
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `FLASK_ENV`: Set to `production`

**Optional Variables:**
- `PORT`: Railway sets this automatically (usually 3000-8000)
- `UPLOAD_FOLDER`: Custom upload directory (default: `uploads`)

### 4. Custom Domain (Optional)
1. In Railway dashboard, go to Settings → Domains
2. Add your custom domain
3. Configure DNS records as shown

## Environment Variables Setup

### OPENROUTER_API_KEY
1. Get your API key from [OpenRouter](https://openrouter.ai/)
2. In Railway: Project → Variables → Add Variable
3. Name: `OPENROUTER_API_KEY`
4. Value: Your API key

### FLASK_ENV
- Name: `FLASK_ENV`
- Value: `production`

## Testing Your Deployment

### Health Check
```bash
curl https://your-app.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-08-07T...",
  "service": "Medical Diagnostics API"
}
```

### n8n Integration
Your Railway URL can be used in n8n workflows:
```
POST https://your-app.railway.app/generate-pdf
```

## Railway-Specific Features

### Auto-Deploy
- Railway automatically redeploys when you push to your connected Git branch
- Check deployment logs in Railway dashboard

### Scaling
- Railway handles auto-scaling based on traffic
- Monitor usage in the Metrics tab

### Logs
- View real-time logs in Railway dashboard
- Use for debugging deployment issues

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check `requirements_api.txt` for correct dependencies
   - Verify Python version in `runtime.txt`
   - Check Railway build logs

2. **Environment Variable Issues**
   - Ensure `OPENROUTER_API_KEY` is set correctly
   - Verify variable names match your code

3. **File Upload Issues**
   - Railway has ephemeral file systems
   - Files are deleted on app restart
   - Consider using cloud storage for production

4. **Memory Issues**
   - Railway free tier has memory limits
   - Optimize PDF generation for large files
   - Consider upgrading plan for heavy usage

### Debug Tips

1. **Check Logs**
   ```bash
   railway logs
   ```

2. **Test Locally First**
   ```bash
   pip install -r requirements_api.txt
   python app.py
   ```

3. **Environment Variables**
   ```bash
   railway variables
   ```

## Production Considerations

### Security
- Never commit API keys to Git
- Use Railway environment variables
- Consider adding authentication for production use

### Performance
- Railway free tier is suitable for development/testing
- Upgrade to paid plan for production traffic
- Monitor response times and memory usage

### File Storage
- Railway has ephemeral storage
- For production, consider:
  - AWS S3 for file uploads
  - Database for persistent data
  - Redis for caching

## Railway vs Other Platforms

### Advantages of Railway
- ✅ Simple deployment process
- ✅ Automatic HTTPS
- ✅ Built-in monitoring
- ✅ Auto-scaling
- ✅ Git integration

### Considerations
- Files are not persistent (use cloud storage)
- Free tier limitations
- May need database service for scaling

## Success Checklist

- [ ] Repository has all required files
- [ ] Environment variables are set
- [ ] Health endpoint responds correctly
- [ ] PDF generation works with test data
- [ ] n8n integration tested
- [ ] Logs show no errors
- [ ] Custom domain configured (if needed)

Your Medical Diagnostics API is now ready for production on Railway! 🚀
