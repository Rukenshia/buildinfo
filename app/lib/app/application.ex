defmodule BuildInfo.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      BuildInfoWeb.Telemetry,
      BuildInfo.Repo,
      {DNSCluster, query: Application.get_env(:app, :dns_cluster_query) || :ignore},
      {Phoenix.PubSub, name: BuildInfo.PubSub},
      # Start the Finch HTTP client for sending emails
      {Finch, name: BuildInfo.Finch},
      # Start a worker by calling: BuildInfo.Worker.start_link(arg)
      # {BuildInfo.Worker, arg},
      # Start to serve requests, typically the last entry
      BuildInfoWeb.Endpoint
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: BuildInfo.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  @impl true
  def config_change(changed, _new, removed) do
    BuildInfoWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
