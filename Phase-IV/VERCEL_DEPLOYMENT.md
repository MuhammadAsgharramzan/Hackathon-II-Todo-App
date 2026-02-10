# Frontend Deployment to Vercel

## Prerequisites
- Vercel account (sign up at https://vercel.com)
- GitHub repository with your code

## Deployment Steps

### Method 1: Deploy via Vercel Dashboard (Easiest)

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/new
   - Click "Import Project"

2. **Import from GitHub**
   - Select your repository: `MuhammadAsgharramzan/Hackathon-II-Todo-App`
   - Click "Import"

3. **Configure Project**
   ```
   Framework Preset: Next.js
   Root Directory: Phase-II/frontend
   Build Command: npm run build (auto-detected)
   Output Directory: .next (auto-detected)
   Install Command: npm install (auto-detected)
   ```

4. **Environment Variables**
   Add this environment variable:
   ```
   NEXT_PUBLIC_API_BASE_URL = https://muhammadasghar-hackathon-ii-todo-app.hf.space
   ```

   **Important**: Replace with your actual HF Space URL (remove any trailing slashes)

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for build to complete
   - Your app will be live at: `https://your-project.vercel.app`

### Method 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend directory
cd Phase-II/frontend

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? todo-app-hackathon
# - Directory? ./
# - Override settings? No

# Add environment variable
vercel env add NEXT_PUBLIC_API_BASE_URL

# When prompted, enter:
# https://muhammadasghar-hackathon-ii-todo-app.hf.space

# Deploy to production
vercel --prod
```

## Post-Deployment Configuration

### 1. Update CORS in Backend

Your HF Space backend needs to allow requests from Vercel. The backend should already have CORS configured, but verify it includes your Vercel domain.

### 2. Test the Deployment

1. **Visit your Vercel URL**
   - Example: `https://todo-app-hackathon.vercel.app`

2. **Test Registration**
   - Click "Register" or "Sign Up"
   - Create a new account
   - Should successfully register

3. **Test Login**
   - Login with your credentials
   - Should redirect to tasks page

4. **Test Task Management**
   - Add a task manually
   - Mark as complete
   - Delete a task

5. **Test Chatbot**
   - Use the chat interface
   - Try: "Add a task: Buy groceries"
   - Try: "List all my tasks"
   - Try: "Complete task 1"

## Troubleshooting

### Issue: "Failed to fetch" or CORS errors

**Solution**: Check that `NEXT_PUBLIC_API_BASE_URL` is set correctly:
```bash
# In Vercel dashboard:
Settings → Environment Variables → Check the value
```

### Issue: Backend not responding

**Solution**: Check HF Space status:
1. Go to https://huggingface.co/spaces/MuhammadAsghar/Hackathon-II-Todo_app
2. Check if Space is "Running"
3. Check logs for errors
4. Verify all secrets are set

### Issue: Database connection errors

**Solution**: Verify DATABASE_URL secret:
1. Check HF Space Settings → Repository secrets
2. Ensure DATABASE_URL is correctly formatted
3. Test database connection from Neon/Supabase dashboard

### Issue: Chatbot not working

**Solution**: Check GEMINI_API_KEY:
1. Verify API key is valid
2. Check HF Space logs for API errors
3. Ensure model name is "gemini-3-flash-preview"

## Environment Variables Reference

### Frontend (Vercel)
```
NEXT_PUBLIC_API_BASE_URL = https://muhammadasghar-hackathon-ii-todo-app.hf.space
```

### Backend (HF Space Secrets)
```
GEMINI_API_KEY = your_gemini_api_key
JWT_SECRET_KEY = your_secure_random_string
DATABASE_URL = postgresql://user:pass@host:5432/dbname
```

## Vercel Deployment Settings

```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "outputDirectory": ".next"
}
```

## Custom Domain (Optional)

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Update CORS in backend if needed

## Continuous Deployment

Vercel automatically redeploys when you push to your GitHub repository:
- Push to `main` branch → Production deployment
- Push to other branches → Preview deployments

## Monitoring

- **Vercel Analytics**: Dashboard → Analytics
- **HF Space Logs**: Space page → Logs tab
- **Database Monitoring**: Neon/Supabase dashboard

## Success Checklist

- [ ] Frontend deployed to Vercel
- [ ] Backend running on HF Space
- [ ] Database connected (Neon/Supabase)
- [ ] Environment variables configured
- [ ] CORS working correctly
- [ ] Registration works
- [ ] Login works
- [ ] Task CRUD operations work
- [ ] Chatbot works
- [ ] All features tested end-to-end
