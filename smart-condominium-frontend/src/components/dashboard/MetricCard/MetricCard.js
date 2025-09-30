// Smart Condominium - Componente de métrica
import React from 'react';
import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import { TrendingUp, TrendingDown, Remove } from '@mui/icons-material';
import { motion } from 'framer-motion';

const MetricCard = ({ 
  title, 
  value, 
  change, 
  changeType = 'neutral',
  icon, 
  color = 'primary' 
}) => {
  const getChangeIcon = () => {
    switch (changeType) {
      case 'positive':
        return <TrendingUp fontSize="small" />;
      case 'negative':
        return <TrendingDown fontSize="small" />;
      default:
        return <Remove fontSize="small" />;
    }
  };

  const getChangeColor = () => {
    switch (changeType) {
      case 'positive':
        return 'success';
      case 'negative':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <motion.div
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
    >
      <Card 
        sx={{ 
          height: '100%',
          cursor: 'pointer',
          '&:hover': {
            boxShadow: (theme) => theme.shadows[8],
          },
        }}
      >
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {title}
              </Typography>
              <Typography variant="h4" component="div" sx={{ fontWeight: 600, mb: 1 }}>
                {value}
              </Typography>
              {change && (
                <Chip
                  icon={getChangeIcon()}
                  label={change}
                  size="small"
                  color={getChangeColor()}
                  variant="outlined"
                />
              )}
            </Box>
            <Box
              sx={{
                p: 1,
                borderRadius: 2,
                backgroundColor: `${color}.light`,
                color: `${color}.main`,
              }}
            >
              {icon}
            </Box>
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default MetricCard;