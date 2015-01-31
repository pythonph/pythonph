var React = require('react/addons');
var superagent = require('superagent');
var marked = require('marked');

require('velocity-animate');
require('velocity-animate/velocity.ui');

var Job = React.createClass({
  toggleDetails: function(e) {
    e.preventDefault();
    this.props.onToggleDetails(this.props);
  },
  toggleCompany: function(e) {
    e.preventDefault();
    this.props.onToggleCompany(this.props.company);
  },
  render: function() {
    return (
      <li>
        <div className="row">
          <div className="two-thirds column">
            <h3>
              <a href="#" onClick={this.toggleDetails}>
                {this.props.title}
              </a>
            </h3>
            <span className="location">{this.props.location}</span>
          </div>
          <div className="one-third column">
            <h4>
              <a
                href="#"
                onClick={this.toggleCompany}
              >
                {this.props.company.name}
              </a>
            </h4>
            <span className="user">
              Posted by {this.props.user.name}
            </span>
          </div>
        </div>
      </li>
    );
  }
});

var Content = React.createClass({
  renderDetails: function() {
    var data = this.props.details;
    return data ? (
      <div className="details page" ref="page">
        <h2>{data.title}</h2>
        <div className="row">
          <div className="one-half column">
            <h3>Company</h3>
            <p>{data.company.name}</p>
          </div>
          <div className="one-half column">
            <h3>Location</h3>
            <p>{data.location}</p>
          </div>
        </div>
        <p
          className="description"
          dangerouslySetInnerHTML={{__html: marked(data.description)}}
        />
        <p>
          <a
            className="apply button"
            href={data.application_url}
          >
            Apply for this job
          </a>
        </p>
        <div
          className="close"
          ref="close"
          onClick={this.close}
        >
          &times;
        </div>
      </div>
    ) : null;
  },
  renderCompany: function() {
    var data = this.props.company;
    return data ? (
      <div className="company page" ref="page">
        <h2>{data.name}</h2>
        <p
          className="profile"
          dangerouslySetInnerHTML={{__html: marked(data.profile)}}
        />
        <p>
          <a
            className="homepage button"
            href={data.homepage}
          >
            Homepage
          </a>
        </p>
        <div
          className="close"
          ref="close"
          onClick={this.close}
        >
          &times;
        </div>
      </div>
    ) : null;
  },
  close: function() {
    if (this.props.details) {
      this.props.toggleContent('details')(null);
    } else {
      this.props.toggleContent('company')(null);
    };
  },
  render: function() {
    return this.props.toggled ? (
      <div className="content">
        <div
          className="overlay"
          ref="overlay"
          onClick={this.close}
        />
        {this.renderDetails()}
        {this.renderCompany()}
      </div>
    ) : null;
  }
});

module.exports = React.createClass({
  displayName: 'Jobs',
  getInitialState: function() {
    return {
      jobs: null,
      next: null,
      prev: null,
      details: null,
      company: null,
      toggled: false
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
  componentDidUpdate: function(prevProps, prevState) {
    if (prevState.jobs !== this.state.jobs) {
      Velocity(
        this.refs.jobsList
          .getDOMNode()
          .querySelectorAll('li'),
        'transition.slideLeftIn',
        {
          duration: 500,
          stagger: 250
        }
      );
    }
    if (this.state.toggled) {
      var content = this.refs.content;
      Velocity(
        content.refs.overlay.getDOMNode(),
        'transition.fadeIn',
        {duration: 500}
      );
      Velocity(
        content.refs.close.getDOMNode(),
        'transition.slideUpBigIn',
        {duration: 500}
      );
      Velocity(
        content.refs.page.getDOMNode(),
        'transition.slideDownIn',
        {duration: 500}
      );
    }
  },
  parseJobs: function(res) {
    this.setState({
      jobs: res.body.objects,
      next: res.body.meta.next,
      prev: res.body.meta.previous
    });
  },
  renderJob: function(data) {
    return (
      <Job
        key={data.id}
        onToggleDetails={this.toggle('details')}
        onToggleCompany={this.toggle('company')}
        {...data}
      />
    );
  },
  renderJobs: function() {
    return this.state.jobs ? (
      this.state.jobs.length > 0 ? (
        this.state.jobs.map(this.renderJob)
      ) : (
        <li>No jobs has been posted yet.</li>
      )
    ) : (
      <li>Loading jobs&hellip;</li>
    );
  },
  prevJobs: function() {
    if (this.state.prev) {
      this.setState({jobs: null});
      superagent
        .get(this.state.prev)
        .end(this.parseJobs);
    }
  },
  nextJobs: function() {
    if (this.state.next) {
      this.setState({jobs: null});
      superagent
        .get(this.state.next)
        .end(this.parseJobs);
    }
  },
  toggle: function(type) {
    return (function(data) {
      var nextToggled = !this.state.toggled;
      var update = (function() {
        var nextState = {toggled: nextToggled};
        nextState[type] = nextToggled ? data : null;
        this.setState(nextState);
      }).bind(this);
      if (nextToggled) {
        update();
      } else {
        var content = this.refs.content;
        Velocity(
          content.refs.overlay.getDOMNode(),
          'transition.fadeOut',
          {duration: 500}
        );
        Velocity(
          content.refs.close.getDOMNode(),
          'transition.slideUpBigOut',
          {duration: 500}
        );
        Velocity(
          content.refs.page.getDOMNode(),
          'transition.slideDownOut',
          {duration: 500, complete: update}
        );
      }
    }).bind(this);
  },
  render: function() {
    var cx = React.addons.classSet;
    var paginationClasses = cx({
      'pagination u-full-width u-cf': true,
      'pagination-hidden': !this.state.prev && !this.state.next
    });
    return (
      <div>
        <Content
          ref="content"
          toggleContent={this.toggle}
          {...this.state}
        />
        <ul
          ref="jobsList"
          className="jobs"
        >
          {this.renderJobs()}
        </ul>
        <div className={paginationClasses}>
          <button
            className="u-pull-left"
            onClick={this.prevJobs}
            disabled={!this.state.prev}
          >
            Previous
          </button>
          <button
            className="u-pull-right"
            onClick={this.nextJobs}
            disabled={!this.state.next}
          >
            Next
          </button>
        </div>
      </div>
    );
  }
});
