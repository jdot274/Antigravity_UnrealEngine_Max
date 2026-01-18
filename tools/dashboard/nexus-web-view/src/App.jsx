import React, { Suspense } from 'react';
import Spline from '@splinetool/react-spline';

export default function App() {
  return (
    <div style={{ width: '100vw', height: '100vh', background: '#000000' }}>
      <Suspense fallback={<div style={{ color: 'white', textAlign: 'center', paddingTop: '50vh' }}>Loading 3D Experience...</div>}>
        <Spline scene="https://prod.spline.design/6Wq1Q7YGyM-iab9i/scene.splinecode" />
      </Suspense>

      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '20px',
        color: 'white',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
        pointerEvents: 'none',
        opacity: 0.7
      }}>
        <h1>Nexus 3D</h1>
        <p>Interactive Asset Viewer</p>
      </div>
    </div>
  );
}
