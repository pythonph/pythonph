var React = require('react/addons');
var superagent = require('superagent');

var Job = React.createClass({
  getInitialState: function() {
    return {
      toggled: false
    };
  },
  toggleDetails: function() {
    this.setState({toggled: !this.state.toggled});
  },
  renderDetails: function() {
    return this.state.toggled ? (
      <div className="details">
        <p className="description">{this.props.description}</p>
        <p>
          <a className="button" href={this.props.application_url}>
            Apply for this job
          </a>
        </p>
      </div>
    ) : null;
  },
  render: function() {
    return (
      <li
        onClick={this.toggleDetails}
      >
        <div className="row">
          <div className="two-thirds column">
            <h2><a href="#">{this.props.title}</a></h2>
            <span className="location">{this.props.location}</span>
            {this.renderDetails()}
          </div>
          <div className="one-third column">
            <h3>{this.props.company.name}</h3>
            <span className="user">
              Posted by {this.props.user.name}
            </span>
          </div>
        </div>
      </li>
    );
  }
});

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
    return <Job key={data.id} {...data} />
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
