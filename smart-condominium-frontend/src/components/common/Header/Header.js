// Smart Condominium - Header/AppBar
import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Avatar,
  Menu,
  MenuItem,
  Badge,
  Tooltip,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications,
  AccountCircle,
  ExitToApp,
  Business,
  Settings,
} from '@mui/icons-material';

import { useAuth } from '../../../contexts/AuthContext';
import { getInitials, stringToColor } from '../../../utils/helpers';

const Header = ({ onMenuClick, sidebarOpen }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const { user, logout } = useAuth();

  const [anchorEl, setAnchorEl] = useState(null);
  const [notificationsAnchor, setNotificationsAnchor] = useState(null);

  // Estado del menú de usuario
  const isMenuOpen = Boolean(anchorEl);
  const isNotificationsOpen = Boolean(notificationsAnchor);

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleNotificationsOpen = (event) => {
    setNotificationsAnchor(event.currentTarget);
  };

  const handleNotificationsClose = () => {
    setNotificationsAnchor(null);
  };

  const handleLogout = async () => {
    handleMenuClose();
    await logout();
    navigate('/login');
  };

  const handleProfile = () => {
    handleMenuClose();
    navigate('/profile');
  };

  // Obtener el título de la página actual
  const getPageTitle = () => {
    const path = location.pathname;
    const titleMap = {
      '/dashboard': 'Dashboard',
      '/profile': 'Mi Perfil',
      '/finance': 'Finanzas',
      '/communication': 'Comunicación',
      '/reservations': 'Reservas',
      '/security': 'Seguridad',
      '/maintenance': 'Mantenimiento',
    };

    for (const [route, title] of Object.entries(titleMap)) {
      if (path.startsWith(route)) {
        return title;
      }
    }
    return 'Smart Condominium';
  };

  const userInitials = user ? getInitials(`${user.first_name} ${user.last_name}`) : 'U';
  const userColor = user ? stringToColor(`${user.first_name} ${user.last_name}`) : '#1565C0';

  return (
    <>
      <AppBar
        position="fixed"
        sx={{
          zIndex: theme.zIndex.drawer + 1,
          background: 'linear-gradient(135deg, #1565C0 0%, #0D47A1 100%)',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        }}
      >
        <Toolbar>
          {/* Botón de menú */}
          <IconButton
            color="inherit"
            aria-label="toggle drawer"
            onClick={onMenuClick}
            edge="start"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>

          {/* Logo y título */}
          <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
            <Business sx={{ mr: 1, fontSize: 28 }} />
            <Box>
              <Typography variant="h6" noWrap component="div">
                Smart Condominium
              </Typography>
              {!isMobile && (
                <Typography variant="caption" sx={{ opacity: 0.8 }}>
                  {getPageTitle()}
                </Typography>
              )}
            </Box>
          </Box>

          {/* Controles del usuario */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {/* Notificaciones */}
            <Tooltip title="Notificaciones">
              <IconButton
                color="inherit"
                onClick={handleNotificationsOpen}
                aria-label="notifications"
              >
                <Badge badgeContent={3} color="error">
                  <Notifications />
                </Badge>
              </IconButton>
            </Tooltip>

            {/* Avatar del usuario */}
            <Tooltip title="Mi cuenta">
              <IconButton
                onClick={handleProfileMenuOpen}
                aria-label="account"
                color="inherit"
              >
                <Avatar
                  sx={{
                    width: 32,
                    height: 32,
                    backgroundColor: userColor,
                    fontSize: '0.875rem',
                    fontWeight: 600,
                  }}
                >
                  {userInitials}
                </Avatar>
              </IconButton>
            </Tooltip>
          </Box>
        </Toolbar>
      </AppBar>

      {/* Menú de usuario */}
      <Menu
        anchorEl={anchorEl}
        id="account-menu"
        open={isMenuOpen}
        onClose={handleMenuClose}
        onClick={handleMenuClose}
        PaperProps={{
          elevation: 3,
          sx: {
            mt: 1.5,
            minWidth: 200,
            '& .MuiAvatar-root': {
              width: 32,
              height: 32,
              ml: -0.5,
              mr: 1,
            },
          },
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <MenuItem onClick={handleProfile}>
          <AccountCircle sx={{ mr: 2 }} />
          Mi Perfil
        </MenuItem>
        <MenuItem onClick={handleMenuClose}>
          <Settings sx={{ mr: 2 }} />
          Configuración
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          <ExitToApp sx={{ mr: 2 }} />
          Cerrar Sesión
        </MenuItem>
      </Menu>

      {/* Menú de notificaciones */}
      <Menu
        anchorEl={notificationsAnchor}
        id="notifications-menu"
        open={isNotificationsOpen}
        onClose={handleNotificationsClose}
        PaperProps={{
          elevation: 3,
          sx: {
            mt: 1.5,
            minWidth: 300,
            maxHeight: 400,
          },
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <MenuItem onClick={handleNotificationsClose}>
          <Box>
            <Typography variant="body2" sx={{ fontWeight: 500 }}>
              Pago vencido
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Su cuota de mantenimiento está vencida
            </Typography>
          </Box>
        </MenuItem>
        <MenuItem onClick={handleNotificationsClose}>
          <Box>
            <Typography variant="body2" sx={{ fontWeight: 500 }}>
              Nueva reserva aprobada
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Su reserva del salón de eventos fue aprobada
            </Typography>
          </Box>
        </MenuItem>
        <MenuItem onClick={handleNotificationsClose}>
          <Box>
            <Typography variant="body2" sx={{ fontWeight: 500 }}>
              Mantenimiento programado
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Mantenimiento de ascensores mañana 9:00 AM
            </Typography>
          </Box>
        </MenuItem>
      </Menu>
    </>
  );
};

export default Header;