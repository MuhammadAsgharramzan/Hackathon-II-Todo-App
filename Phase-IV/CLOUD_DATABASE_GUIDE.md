# Cloud Database Deployment Guide

## Overview

This guide explains how to deploy the Todo App using a cloud-managed PostgreSQL database (Neon) instead of a local Docker Postgres container.

## Benefits of Cloud Database

- **Managed Service**: No need to manage database backups, updates, or scaling
- **High Availability**: Built-in redundancy and failover
- **Scalability**: Easily scale database resources as needed
- **Reduced Local Resources**: Lighter local deployment without Postgres container
- **Production-Ready**: Suitable for production deployments

## Prerequisites

- Neon PostgreSQL database (or other cloud Postgres provider)
- Database connection string
- Docker images built: `todo-backend:latest` and `todo-frontend:latest`

## Deployment Steps

### Option 1: Using docker-compose.cloud.yml

This is the simplest approach for cloud database deployment.

```bash
# 1. Navigate to Phase-IV directory
cd Phase-IV

# 2. Deploy with cloud configuration
docker-compose -f docker-compose.cloud.yml up -d

# 3. Verify services are running
docker-compose -f docker-compose.cloud.yml ps

# 4. Check logs
docker-compose -f docker-compose.cloud.yml logs -f
```

**Access**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Option 2: Using .env.production

If you want to customize the configuration:

```bash
# 1. Copy production environment template
cp .env.production .env

# 2. Edit .env with your database credentials
nano .env

# 3. Update docker-compose.yml to use environment file
# (Already configured to read from .env)

# 4. Remove postgres service from docker-compose.yml
# Comment out or remove the postgres service section

# 5. Deploy
docker-compose up -d
```

## Configuration Details

### Database Connection String Format

```
postgresql://[user]:[password]@[host]:[port]/[database]?sslmode=require
```

**Example** (Neon PostgreSQL):
```
postgresql://neondb_owner:npg_eh09qfTDmuRw@ep-gentle-feather-aiiy5n8h-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### Environment Variables

The following environment variables are required:

**Backend**:
- `DATABASE_URL`: Full PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `GEMINI_API_KEY`: API key for Gemini AI service
- `PORT`: Backend port (default: 8000)

**Frontend**:
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL
- `NODE_ENV`: Environment (production/development)
- `PORT`: Frontend port (default: 3000)

## Security Considerations

### ⚠️ Important Security Notes

1. **Never commit credentials to Git**:
   - `.env` files are in `.gitignore`
   - Use `.env.production` as a template only
   - Replace placeholder values with real credentials

2. **Rotate secrets for production**:
   ```bash
   # Generate new JWT secret
   openssl rand -hex 32
   ```

3. **Use SSL/TLS**:
   - Always use `sslmode=require` for database connections
   - Configure HTTPS for frontend in production

4. **Restrict database access**:
   - Configure firewall rules to allow only your application IPs
   - Use connection pooling (Neon provides this automatically)

## Database Migration

If migrating from local Postgres to cloud database:

### Export from Local Database

```bash
# 1. Export data from local Postgres
docker exec todo-postgres pg_dump -U todo_user todo_db > backup.sql

# 2. Connect to Neon database
psql "postgresql://neondb_owner:npg_eh09qfTDmuRw@ep-gentle-feather-aiiy5n8h-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"

# 3. Import data
\i backup.sql
```

### Verify Migration

```bash
# Check backend readiness (includes DB connectivity test)
curl http://localhost:8000/ready

# Expected response:
# {"status":"ready","database":"connected"}
```

## Troubleshooting

### Connection Refused

**Problem**: Backend cannot connect to database

**Solutions**:
1. Verify database URL is correct
2. Check database firewall rules allow your IP
3. Ensure SSL mode is set correctly
4. Check database is running (Neon dashboard)

```bash
# Test connection manually
docker exec todo-backend python -c "
from sqlalchemy import create_engine
engine = create_engine('postgresql://...')
with engine.connect() as conn:
    print('Connected successfully')
"
```

### SSL Certificate Errors

**Problem**: SSL verification fails

**Solutions**:
1. Ensure `sslmode=require` is in connection string
2. For self-signed certificates, use `sslmode=verify-ca`
3. Check system CA certificates are up to date

### Performance Issues

**Problem**: Slow database queries

**Solutions**:
1. Check Neon dashboard for query performance
2. Enable connection pooling (already enabled in Neon)
3. Add database indexes for frequently queried fields
4. Consider upgrading Neon plan for more resources

## Monitoring

### Health Checks

The backend `/ready` endpoint checks database connectivity:

```bash
# Continuous monitoring
watch -n 5 'curl -s http://localhost:8000/ready | jq'
```

### Database Metrics

Monitor database performance in Neon dashboard:
- Connection count
- Query performance
- Storage usage
- CPU/Memory usage

## Scaling

### Horizontal Scaling

With cloud database, you can scale application containers independently:

```bash
# Scale backend to 3 replicas
docker-compose -f docker-compose.cloud.yml up -d --scale backend=3

# Scale frontend to 2 replicas
docker-compose -f docker-compose.cloud.yml up -d --scale frontend=2
```

### Database Scaling

Neon provides automatic scaling:
- **Compute**: Auto-scales based on load
- **Storage**: Auto-scales as data grows
- **Connections**: Connection pooling handles concurrent requests

## Cost Optimization

### Neon Free Tier

- 0.5 GB storage
- Shared compute
- Suitable for development/testing

### Production Recommendations

1. **Use connection pooling**: Reduces connection overhead
2. **Enable auto-suspend**: Database suspends when inactive
3. **Monitor usage**: Track storage and compute usage
4. **Optimize queries**: Add indexes, use efficient queries

## Backup and Recovery

### Automated Backups

Neon provides automatic backups:
- Point-in-time recovery (PITR)
- Retention: 7 days (free tier), 30 days (paid)

### Manual Backup

```bash
# Create manual backup
pg_dump "postgresql://..." > backup_$(date +%Y%m%d).sql

# Restore from backup
psql "postgresql://..." < backup_20260210.sql
```

## Switching Between Local and Cloud

### To Cloud Database

```bash
docker-compose down
docker-compose -f docker-compose.cloud.yml up -d
```

### To Local Database

```bash
docker-compose -f docker-compose.cloud.yml down
docker-compose up -d
```

## Production Checklist

Before deploying to production with cloud database:

- [ ] Rotate all secrets (JWT, API keys)
- [ ] Configure database firewall rules
- [ ] Enable SSL/TLS for all connections
- [ ] Set up monitoring and alerting
- [ ] Configure automated backups
- [ ] Test disaster recovery procedures
- [ ] Document connection strings securely
- [ ] Set up CI/CD pipeline
- [ ] Configure rate limiting
- [ ] Enable logging and audit trails

## Support

For issues with:
- **Neon Database**: https://neon.tech/docs
- **Application**: Check logs with `docker-compose logs`
- **Deployment**: Refer to main DEPLOYMENT_GUIDE.md

## Next Steps

1. Deploy with cloud database configuration
2. Run integration tests to verify connectivity
3. Monitor performance and resource usage
4. Set up production monitoring (Prometheus/Grafana)
5. Configure CI/CD for automated deployments
