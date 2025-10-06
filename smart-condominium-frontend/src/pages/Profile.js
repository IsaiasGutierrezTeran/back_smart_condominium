// Smart Condominium - Página de Perfil
import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  Avatar,
  Divider,
  Alert,
} from '@mui/material';
import { Edit, Save, Cancel } from '@mui/icons-material';
import { motion } from 'framer-motion';

import { useAuth } from '../contexts/AuthContext';
import { getInitials, stringToColor } from '../utils/helpers';
import LoadingSpinner from '../components/common/LoadingSpinner/LoadingSpinner';

const Profile = () => {
  const { user, updateProfile, loading } = useAuth();
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    email: user?.email || '',
    telefono: user?.telefono || '',
    direccion: user?.direccion || '',
  });
  const [message, setMessage] = useState({ type: '', text: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const result = await updateProfile(formData);
    
    if (result.success) {
      setEditMode(false);
      setMessage({ type: 'success', text: 'Perfil actualizado exitosamente' });
    } else {
      setMessage({ type: 'error', text: result.error });
    }
    
    setTimeout(() => setMessage({ type: '', text: '' }), 5000);
  };

  const handleCancel = () => {
    setFormData({
      first_name: user?.first_name || '',
      last_name: user?.last_name || '',
      email: user?.email || '',
      telefono: user?.telefono || '',
      direccion: user?.direccion || '',
    });
    setEditMode(false);
  };

  const userInitials = user ? getInitials(`${user.first_name} ${user.last_name}`) : 'U';
  const userColor = user ? stringToColor(`${user.first_name} ${user.last_name}`) : '#1565C0';

  return (
    <Container maxWidth="md">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600, mb: 4 }}>
          Mi Perfil
        </Typography>

        {message.text && (
          <Alert severity={message.type} sx={{ mb: 3 }}>
            {message.text}
          </Alert>
        )}

        <Grid container spacing={3}>
          {/* Información básica */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent sx={{ textAlign: 'center', p: 4 }}>
                <Avatar
                  sx={{
                    width: 120,
                    height: 120,
                    backgroundColor: userColor,
                    fontSize: '2rem',
                    fontWeight: 600,
                    mx: 'auto',
                    mb: 2,
                  }}
                >
                  {userInitials}
                </Avatar>
                
                <Typography variant="h5" component="h2" gutterBottom>
                  {user ? `${user.first_name} ${user.last_name}` : 'Usuario'}
                </Typography>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {user?.username}
                </Typography>
                
                <Typography variant="body2" color="text.secondary">
                  {user?.rol ? user.rol.charAt(0).toUpperCase() + user.rol.slice(1) : 'Residente'}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Formulario de perfil */}
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                  <Typography variant="h6" component="h3">
                    Información Personal
                  </Typography>
                  
                  {!editMode ? (
                    <Button
                      startIcon={<Edit />}
                      onClick={() => setEditMode(true)}
                      variant="outlined"
                    >
                      Editar
                    </Button>
                  ) : (
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <Button
                        startIcon={<Save />}
                        onClick={handleSubmit}
                        variant="contained"
                        disabled={loading}
                      >
                        {loading ? <LoadingSpinner size={20} /> : 'Guardar'}
                      </Button>
                      <Button
                        startIcon={<Cancel />}
                        onClick={handleCancel}
                        variant="outlined"
                        disabled={loading}
                      >
                        Cancelar
                      </Button>
                    </Box>
                  )}
                </Box>

                <Divider sx={{ mb: 3 }} />

                <Box component="form" onSubmit={handleSubmit}>
                  <Grid container spacing={3}>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        name="first_name"
                        label="Nombre"
                        value={formData.first_name}
                        onChange={handleChange}
                        disabled={!editMode || loading}
                        variant={editMode ? "outlined" : "standard"}
                        InputProps={{
                          readOnly: !editMode,
                        }}
                      />
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        name="last_name"
                        label="Apellido"
                        value={formData.last_name}
                        onChange={handleChange}
                        disabled={!editMode || loading}
                        variant={editMode ? "outlined" : "standard"}
                        InputProps={{
                          readOnly: !editMode,
                        }}
                      />
                    </Grid>
                    
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        name="email"
                        label="Email"
                        type="email"
                        value={formData.email}
                        onChange={handleChange}
                        disabled={!editMode || loading}
                        variant={editMode ? "outlined" : "standard"}
                        InputProps={{
                          readOnly: !editMode,
                        }}
                      />
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        name="telefono"
                        label="Teléfono"
                        value={formData.telefono}
                        onChange={handleChange}
                        disabled={!editMode || loading}
                        variant={editMode ? "outlined" : "standard"}
                        InputProps={{
                          readOnly: !editMode,
                        }}
                      />
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        name="direccion"
                        label="Dirección"
                        value={formData.direccion}
                        onChange={handleChange}
                        disabled={!editMode || loading}
                        variant={editMode ? "outlined" : "standard"}
                        InputProps={{
                          readOnly: !editMode,
                        }}
                      />
                    </Grid>
                  </Grid>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </motion.div>
    </Container>
  );
};

export default Profile;