var React = require('react/addons');
var superagent = require('superagent');

module.exports = React.createClass({
  displayName: 'Jobs',
  getInitialState: function() {
    return {
      jobs: null
    };
  },
  apiUrl: function() {
    return ['/api', this.props.apiVersion].concat(
      Array.prototype.slice.call(arguments)
    ).join('/');
  },
  componentDidMount: function() {
    superagent
      .get(this.apiUrl('job'))
      .end(this.parseJobs);
  },
  parseJobs: function(res) {
    this.setState({
      jobs: res.body.objects
    });
  },
  renderJob: function(data) {
    return (
      <li key={data.id}>
        <div className="row">
          <div className="two-thirds column">
            <h2>{data.title}</h2>
            <span className="location">{data.location}</span>
          </div>
          <div className="one-third column">
            <h3>{data.company.name}</h3>
            <span className="user">
              Posted by {data.user.name}
            </span>
          </div>
        </div>
      </li>
    );
  },
  renderJobs: function() {
    return this.state.jobs ? (
      this.state.jobs.map(this.renderJob)
    ) : (
      <li>Loading jobs&hellip;</li>
    );
  },
  render: function() {
    return typeof this.state.jobs === null ? (
      <p>No jobs has been posted yet.</p>
    ) : (
      <ul className="jobs">
        {this.renderJobs()}
      </ul>
    );
  }
});
