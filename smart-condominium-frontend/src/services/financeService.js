// Smart Condominium - Servicio de Finanzas
import api, { handleApiError, createPaginatedRequest } from './api';

class FinanceService {
  // Obtener mis pagos (residente)
  async getMyPayments(params = {}) {
    try {
      const response = await createPaginatedRequest('/api/finanzas/mis-pagos/', params.page, params.pageSize, params);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Obtener historial de pagos del usuario
  async getMyPaymentHistory(params = {}) {
    try {
      const response = await api.get('/api/finanzas/historial/', { params });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Obtener resumen financiero del usuario
  async getMyFinancialSummary() {
    try {
      const response = await api.get('/api/finanzas/resumen/');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Obtener todos los pagos (administrador)
  async getAllPayments(params = {}) {
    try {
      const response = await createPaginatedRequest('/api/finanzas/pagos/', params.page, params.pageSize, params);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Obtener detalle de un pago
  async getPayment(paymentId) {
    try {
      const response = await api.get(`/api/finanzas/pagos/${paymentId}/`);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Procesar pago
  async processPayment(paymentId, paymentData) {
    try {
      const response = await api.post(`/api/finanzas/pagos/${paymentId}/procesar/`, paymentData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Generar pagos mensuales
  async generateMonthlyPayments(data) {
    try {
      const response = await api.post('/api/finanzas/generar-pagos/', data);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Obtener unidades habitacionales
  async getUnits(params = {}) {
    try {
      const response = await createPaginatedRequest('/api/finanzas/unidades/', params.page, params.pageSize, params);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Obtener detalle de unidad habitacional
  async getUnit(unitId) {
    try {
      const response = await api.get(`/api/finanzas/unidades/${unitId}/`);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Crear unidad habitacional
  async createUnit(unitData) {
    try {
      const response = await api.post('/api/finanzas/unidades/', unitData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Actualizar unidad habitacional
  async updateUnit(unitId, unitData) {
    try {
      const response = await api.patch(`/api/finanzas/unidades/${unitId}/`, unitData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Eliminar unidad habitacional
  async deleteUnit(unitId) {
    try {
      await api.delete(`/api/finanzas/unidades/${unitId}/`);
      return {
        success: true,
        message: 'Unidad eliminada exitosamente',
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Obtener tipos de pago
  async getPaymentTypes() {
    try {
      const response = await api.get('/api/finanzas/tipos-pago/');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Obtener multas
  async getFines(params = {}) {
    try {
      const response = await createPaginatedRequest('/api/finanzas/multas/', params.page, params.pageSize, params);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Obtener detalle de multa
  async getFine(fineId) {
    try {
      const response = await api.get(`/api/finanzas/multas/${fineId}/`);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Crear multa
  async createFine(fineData) {
    try {
      const response = await api.post('/api/finanzas/multas/', fineData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Actualizar multa
  async updateFine(fineId, fineData) {
    try {
      const response = await api.patch(`/api/finanzas/multas/${fineId}/`, fineData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Eliminar multa
  async deleteFine(fineId) {
    try {
      await api.delete(`/api/finanzas/multas/${fineId}/`);
      return {
        success: true,
        message: 'Multa eliminada exitosamente',
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Aplicar intereses moratorios
  async applyLateFees(data) {
    try {
      const response = await api.post('/api/finanzas/aplicar-intereses/', data);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Obtener resumen financiero (administrador)
  async getAdminFinancialSummary(params = {}) {
    try {
      const response = await api.get('/api/finanzas/resumen-admin/', { params });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Obtener reporte de morosidad
  async getDelinquencyReport(params = {}) {
    try {
      const response = await api.get('/api/finanzas/reporte-morosidad/', { params });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Exportar reporte financiero
  async exportFinancialReport(params = {}) {
    try {
      const response = await api.get('/api/finanzas/exportar-reporte/', {
        params,
        responseType: 'blob',
      });
      
      // Crear URL para descargar
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.download = `reporte_financiero_${new Date().toISOString().split('T')[0]}.xlsx`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      return {
        success: true,
        message: 'Reporte descargado exitosamente',
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }

  // Obtener estadísticas de pagos
  async getPaymentStatistics(params = {}) {
    try {
      const response = await api.get('/api/finanzas/estadisticas-pagos/', { params });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: handleApiError(error),
      };
    }
  }
}

export default new FinanceService();