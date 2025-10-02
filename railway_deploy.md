# Deploying wger to Railway

This guide will help you deploy the wger (Workout Manager) application to Railway.

## Prerequisites

1. A Railway account (sign up at [railway.app](https://railway.app))
2. Railway CLI installed locally
3. Git repository access

## Step 1: Install Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Or using curl
curl -fsSL https://railway.app/install.sh | sh
```

## Step 2: Login to Railway

```bash
railway login
```

## Step 3: Initialize Railway Project

```bash
# In your wger project directory
railway init
```

## Step 4: Add Required Services

### Add PostgreSQL Database
```bash
railway add postgresql
```

### Add Redis (Optional, for caching)
```bash
railway add redis
```

## Step 5: Configure Environment Variables

Set the following environment variables in Railway:

```bash
# Required settings
railway variables set SECRET_KEY="your-super-secret-key-here"
railway variables set DJANGO_DEBUG=False
railway variables set DJANGO_SETTINGS_MODULE=railway_settings

# Database (automatically set by Railway PostgreSQL service)
# PGDATABASE, PGUSER, PGPASSWORD, PGHOST, PGPORT are set automatically

# Redis (if using Redis service)
railway variables set REDIS_URL="redis://localhost:6379/1"

# Application settings
railway variables set ALLOW_GUEST_USERS=True
railway variables set ALLOW_REGISTRATION=True
railway variables set ALLOW_UPLOAD_VIDEOS=False

# Email settings (optional)
railway variables set SMTP_HOST="your-smtp-host"
railway variables set SMTP_PORT=587
railway variables set SMTP_USE_TLS=True
railway variables set SMTP_USER="your-email@example.com"
railway variables set SMTP_PASSWORD="your-email-password"

# Security settings
railway variables set CSRF_TRUSTED_ORIGINS="https://your-app.railway.app"
```

## Step 6: Deploy to Railway

```bash
# Deploy the application
railway up
```

## Step 7: Initialize the Database

After deployment, run the following commands to set up the database:

```bash
# Run migrations
railway run python manage.py migrate

# Load initial data
railway run python manage.py loaddata gym.json
railway run python manage.py loaddata languages.json
railway run python manage.py loaddata groups.json
railway run python manage.py loaddata users.json
railway run python manage.py loaddata licenses.json
railway run python manage.py loaddata setting_repetition_units.json
railway run python manage.py loaddata setting_weight_units.json
railway run python manage.py loaddata gym_config.json
railway run python manage.py loaddata equipment.json
railway run python manage.py loaddata muscles.json
railway run python manage.py loaddata categories.json
railway run python manage.py loaddata exercise-base-data.json
railway run python manage.py loaddata translations.json

# Create admin user
railway run python manage.py createsuperuser

# Set site URL
railway run python manage.py set-site-url
```

## Step 8: Load Additional Data (Optional)

To load exercise images and ingredients data:

```bash
# Download exercise images
railway run python manage.py download-exercise-images

# Load ingredients from Open Food Facts
railway run wger load-online-fixtures

# Sync ingredients
railway run python manage.py sync-ingredients
```

## Step 9: Access Your Application

1. Get your Railway URL:
   ```bash
   railway domain
   ```

2. Visit your application at the provided URL

3. Login with the admin user you created

## Configuration Files

The following files have been created for Railway deployment:

- `railway.json` - Railway deployment configuration
- `Procfile` - Process definition for Railway
- `railway_settings.py` - Railway-specific Django settings
- `requirements.txt` - Python dependencies including Railway-specific packages

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DJANGO_DEBUG` | Debug mode | `False` |
| `DJANGO_SETTINGS_MODULE` | Settings module | `railway_settings` |
| `ALLOW_GUEST_USERS` | Allow guest access | `True` |
| `ALLOW_REGISTRATION` | Allow user registration | `True` |
| `ALLOW_UPLOAD_VIDEOS` | Allow video uploads | `False` |
| `SMTP_HOST` | SMTP server for emails | Optional |
| `SMTP_PORT` | SMTP port | `587` |
| `SMTP_USER` | SMTP username | Optional |
| `SMTP_PASSWORD` | SMTP password | Optional |

## Troubleshooting

### Static Files Not Loading
If static files aren't loading, ensure WhiteNoise is properly configured in `railway_settings.py`.

### Database Connection Issues
Check that PostgreSQL service is properly connected and environment variables are set.

### Memory Issues
Railway has memory limits. If you encounter memory issues:
- Disable Celery (set `USE_CELERY=False`)
- Reduce cache settings
- Optimize static file serving

## Monitoring

Railway provides built-in monitoring and logging. Check the Railway dashboard for:
- Application logs
- Performance metrics
- Error tracking

## Scaling

Railway automatically handles scaling, but you can:
- Upgrade to a higher plan for more resources
- Configure horizontal scaling
- Set up monitoring alerts

## Security Considerations

1. **Change the default SECRET_KEY** - Use a strong, unique secret key
2. **Configure CSRF_TRUSTED_ORIGINS** - Set your Railway domain
3. **Set up proper email configuration** - For user registration and notifications
4. **Regular backups** - Railway provides database backups, but consider additional backup strategies
5. **Monitor access logs** - Keep an eye on unusual activity

## Support

- Railway Documentation: https://docs.railway.app/
- wger Documentation: https://wger.readthedocs.io/
- Railway Discord: https://discord.gg/railway
- wger Discord: https://discord.gg/rPWFv6W
