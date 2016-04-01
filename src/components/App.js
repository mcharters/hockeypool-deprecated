import React from 'react';
import { PageHeader, Input } from 'react-bootstrap';

const App = ({ handleChange }) => (
  <div className="container">
    <PageHeader>Hockey Pool</PageHeader>
    <Input
      type="text"
      label="Enter Team Name:"
      onChange={handleChange}
    />
  </div>
);

export default App;
