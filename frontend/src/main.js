var React = require('react/addons');

var Jobs = require('./jobs');

React.render(
  <Jobs apiVersion={apiVersion} />,
  document.getElementById('jobs')
);
