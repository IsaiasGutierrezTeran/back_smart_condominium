// Smart Condominium - Componente de carga
import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import { motion } from 'framer-motion';

const LoadingSpinner = ({ 
  size = 40, 
  message = '', 
  fullScreen = false,
  color = 'primary' 
}) => {
  const containerProps = fullScreen 
    ? {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(255, 255, 255, 0.8)',
        zIndex: 9999,
      }
    : {};

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 2,
        ...containerProps,
      }}
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <CircularProgress size={size} color={color} />
      </motion.div>
      
      {message && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          <Typography 
            variant="body2" 
            color="text.secondary"
            sx={{ textAlign: 'center' }}
          >
            {message}
          </Typography>
        </motion.div>
      )}
    </Box>
  );
};

export default LoadingSpinner;